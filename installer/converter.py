import installer.parser.execution as execution
import installer.parser.model as parsemodel
import installer.model.build.disk as tablebuilder
import installer.model.model.disk as tablemodel
import installer.model.model.partition as partition
import installer.model.build.partition as pb
import installer.model.build.mount as mb
import installer.model.model.software as sw
import installer.model.build.software as swb
import installer.model.gen.software as swg
import installer.model.model.script as script
import installer.model.model.user as user
import installer.system as system
import installer.model.build.user as userb
import installer.model.model.chroot as chroot
import installer.model.model.network as nw

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
    partDevice = ""
    i = 0
    for part in step.model.partitions:
        i += 1
        if part.bIsEncrypted:
            bIsEncrypted = True
            if "nvme" not in step.model.device:
                partDevice = step.model.device + str(i)
            else:
                partDevice = step.model.device + "p" + str(i)
    return concat(["\n# Generating the bootloader"], script.bootloader(shell="",
                                                                       device=step.model.device,
                                                                       installcommand=config["BOOTLOADER_EFI"],
                                                                       installDOSCommand=config["BOOTLOADER_DOS"],
                                                                       configcommand=config["BOOTLOADER_CONFIG"],
                                                                       bIsGPT=step.model.gpt, bIsEncrypted=bIsEncrypted, kernel=config["KERNEL"], partitionDevice=partDevice).exec())


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
    if model.bGenTable:
        return concat(["\n#Building partition table"], tablebuilder.buildPartitionTable(table))
    return concat(["\n#Building partition table"], tablebuilder.buildPartitionTableEntries(table))


def genPartitions(parserPartitions, diskdevice, config):
    """
    generate a list of model partition from a parser partition model
    """
    partitions = []
    if "nvme" in diskdevice:
        diskdevice += "p"
    # TODO: Generate logic volumes here as well
    for i, part in enumerate(parserPartitions):
        device = diskdevice+str(i+1)
        offset = i+1
        if (part.offset != None):
            device = diskdevice + str(part.offset)
            offset = part.offset
        partitions.append(partition.partition(device,
                                              part.name, part.mount, part.filesystem, part.start, part.end, part.bIsEncrypted, part.volumes, part.password, part.resize, part.size, offset))
    return partitions
