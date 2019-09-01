import parser.execution as execution
import parser.model as parsemodel
import model.build.disk as tablebuilder
import model.model.disk as tablemodel
import model.model.partition as partition
import model.build.partition as pb
import model.build.mount as mb
import model.model.software as sw
import model.build.software as swb
import model.gen.software as swg
import model.model.script as script
import model.model.user as user
import system
import model.build.user as userb
import model.model.chroot as chroot
import model.model.network as nw

conf = None


def concat(list1, list2):
    newList = list1
    for item in list2:
        newList.append(item)
    return newList


def convertYamlToCommands(executor, config=None):
    """
    convert a parser.executor object to commands
    """
    commands = []
    for step in executor.steps:
        # make partitiontable
        if type(step) == type(execution.partitiontable()):
            commands = concat(commands, PartitionTableGen(step, config))
        elif type(step) == type(execution.format()):
            commands = concat(commands, formatGen(step, config))
        elif type(step) == type(execution.mount()):
            commands = concat(commands, mountGen(step, config))
        elif type(step) == type(execution.bootstrap()):
            commands = concat(commands, bootstrapGen(step, config))
        elif type(step) == type(execution.fstab()):
            commands = concat(commands, fstabGen(step, config))
        elif type(step) == type(execution.scriptstep()):
            commands = concat(commands, scriptGen(step, config))
        elif type(step) == type(execution.chroot(config)):
            commands = concat(commands, chrootGen(step, config))
        elif type(step) == type(execution.systemsetup()):
            commands = concat(commands, systemGen(step, config))
        elif type(step) == type(execution.createUser()):
            commands = concat(commands, createUser(step, config))
        elif type(step) == type(execution.bootloaderstep()):
            commands = concat(commands, bootloaderGen(step, config))
        elif type(step) == type(execution.packages()):
            commands = concat(commands, packageGen(step, config))
        elif type(step) == type(execution.network()):
            commands == concat(commands, networkGen(step, config))
        else:
            print(step)
    return commands


def networkGen(step, config):
    """
    If no network exists then we will try and connect to one
    """
    return concat(["\n#Establishing a network connection"], nw.Connector().getShellCommand(step.model.ssid, step.model.password, config["WIFI_CONNECT_COMMAND_WITH_PASSWORD"], config))


def systemGen(step, config):
    return concat(["\n# Setting up system parameters"], system.system(step.model.local, step.model.keymap,
                                                                      step.model.hostname, step.model.password).setup(config))


def createUser(step, config):
    usr = user.user(step.model.name, step.model.password,
                    step.model.groups, step.model.shell)
    return concat(["\n# Creating a user"], userb.makeUnixUser(usr, config))


def bootloaderGen(step, config):
    bIsEncrypted = False
    for part in step.model.partitions:
        if part.bIsEncrypted:
            bIsEncrypted = True
    return concat(["\n# Generating the bootloader"], script.bootloader(shell="",
                                                                       device=step.model.device,
                                                                       installcommand=config["BOOTLOADER_EFI"],
                                                                       installDOSCommand=config["BOOTLOADER_DOS"],
                                                                       configcommand=config["BOOTLOADER_CONFIG"],
                                                                       bIsGPT=step.model.gpt, bIsEncrypted=bIsEncrypted, kernel=config["KERNEL"]).exec())


def packageGen(step, config):
    if step.model.file != None:
        return concat(["\n# Installing software"], swb.installSoftware(swg.BuildSoftwareFromFile(step.model.file, step.model.install)))
    return concat(["\n# Installing software"], swb.installSoftware(sw.software(step.model.install, step.model.packages)))


def chrootGen(step, config):
    """
    Build chroot command from a parser.executor.chroot object
    """
    commands = convertYamlToCommands(step, config)
    return concat(["\n# Executing chroot function"], chroot.chroot(chrootfunc=config["CHROOT"], user=step.user, mountpoint=step.mountpoint).start(command=commands, herefile=config["HERESTRING"]))


def scriptGen(step, config):
    """
    Generate a script command from a parser.executor.script
    """
    if not step.model.command == None:
        return concat(["\n# Executing custom script"], script.script(shell="", payload=step.model.command).exec())
    with open(step.model.file, 'r') as stream:
        return concat(["\n# Executing custom script"], script.script(shell="", payload=stream.read()).exec())


def bootstrapGen(step, config):
    """
    Bootstrap the system on a drive
    """
    return concat(["\n#bootstrapping system"], swb.installSoftware(sw.software(config["BOOTSTRAP"], packages=config["BOOTSTRAP_PACKAGES"])))


def fstabGen(step, config):
    return ["\n# Generate fstab", config["FSTAB"]]


def mountGen(mounter, config):
    """
    Generate mount commands from a parser.executor.mount object
    """
    commands = ["\n#Mounting partitions"]
    if type(mounter.model) == type(parsemodel.disk()):
        partitions = genPartitions(
            mounter.model.partitions, mounter.model.device, config)
    else:
        partitions = genPartitions(
            [mounter.model], mounter.model.device, config)
    commands = concat(commands, mb.mountAll(partitions, config["MOUNTPOINT"]))

    return commands


def formatGen(formater, config):
    """
    Generate format commands from a parser.executor.format object
    """
    commands = ["\n#Formating partitions"]
    if type(formater.model) == type(parsemodel.disk()):
        partitions = genPartitions(
            formater.model.partitions, formater.model.device, config)
    else:
        partitions = genPartitions(
            [formater.model], formater.model.device, config)
    for part in partitions:
        commands = concat(commands, pb.format(part, config))
    return commands


def PartitionTableGen(ptable, config):
    """
    Convert a partitiontable gen step to a list of commands
    """
    model = ptable.model
    table = tablemodel.disk(model.device, model.size,
                            genPartitions(model.partitions, model.device, config), model.gpt)
    return concat(["\n#Building partition table"], tablebuilder.buildPartitionTable(table))


def genPartitions(parserPartitions, diskdevice, config):
    """
    generate a list of model partition from a parser partition model
    """
    partitions = []
    # TODO: Generate logic volumes here as well
    for i, part in enumerate(parserPartitions):
        partitions.append(partition.partition(diskdevice+str(i+1),
                                              part.name, part.mount, part.filesystem, part.start, part.end, part.bIsEncrypted, part.volumes, part.password))
    return partitions
