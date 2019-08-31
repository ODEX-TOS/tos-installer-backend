import config


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


def concat(list1, list2):
    newList = list1
    for item in list2:
        newList.append(item)
    return newList


def convertYamlToCommands(executor):
    """
    convert a parser.executor object to commands
    """
    commands = []
    for step in executor.steps:
        # make partitiontable
        if type(step) == type(execution.partitiontable()):
            commands = concat(commands, PartitionTableGen(step))
        elif type(step) == type(execution.format()):
            commands = concat(commands, formatGen(step))
        elif type(step) == type(execution.mount()):
            commands = concat(commands, mountGen(step))
        elif type(step) == type(execution.bootstrap()):
            commands = concat(commands, bootstrapGen(step))
        elif type(step) == type(execution.fstab()):
            commands = concat(commands, fstabGen(step))
        elif type(step) == type(execution.scriptstep()):
            commands = concat(commands, scriptGen(step))
        elif type(step) == type(execution.chroot()):
            commands = concat(commands, chrootGen(step))
        elif type(step) == type(execution.systemsetup()):
            commands = concat(commands, systemGen(step))
        elif type(step) == type(execution.createUser()):
            commands = concat(commands, createUser(step))
        elif type(step) == type(execution.bootloaderstep()):
            commands = concat(commands, bootloaderGen(step))
        elif type(step) == type(execution.packages()):
            commands = concat(commands, packageGen(step))
        else:
            print(step)
    return commands


def systemGen(step):
    return concat(["\n# Setting up system parameters"], system.system(step.model.local, step.model.keymap,
                                                                      step.model.hostname, step.model.password).setup())


def createUser(step):
    usr = user.user(step.model.name, step.model.password,
                    step.model.groups, step.model.shell)
    return concat(["\n# Creating a user"], userb.makeUnixUser(usr))


def bootloaderGen(step):
    return concat(["\n# Generating the bootloader"], script.bootloader(shell="",
                                                                       device=step.model.device, bIsGPT=step.model.gpt).exec())


def packageGen(step):
    if step.model.file != None:
        return concat(["\n# Installing software"], swb.installSoftware(swg.BuildSoftwareFromFile(step.model.file, step.model.install)))
    return concat(["\n# Installing software"], swb.installSoftware(sw.software(step.model.install, step.model.packages)))


def chrootGen(step):
    """
    Build chroot command from a parser.executor.chroot object
    """
    commands = convertYamlToCommands(step)
    return concat(["\n# Executing chroot function"], chroot.chroot(user=step.user, mountpoint=step.mountpoint).start(command=commands))


def scriptGen(step):
    """
    Generate a script command from a parser.executor.script
    """
    if not step.model.command == None:
        return concat(["\n# Executing custom script"], script.script(shell="", payload=step.model.command).exec())
    with open(step.model.file, 'r') as stream:
        return concat(["\n# Executing custom script"], script.script(shell="", payload=stream.read()).exec())


# Todo: don't hardcode these values -> move to config


def bootstrapGen(step):
    """
    Bootstrap the system on a drive
    """
    return concat(["\n#bootstrapping system"], swb.installSoftware(sw.software("pacstrap --noconfirm /mnt", packages=[
        "base", "base-devel", "efibootmgr", "vim", "dialog", "xterm", "grub"])))


def fstabGen(step):
    return ["\n# Generate fstab", config.FSTAB]


def mountGen(mounter):
    """
    Generate mount commands from a parser.executor.mount object
    """
    commands = ["\n#Mounting partitions"]
    if type(mounter.model) == type(parsemodel.disk()):
        partitions = genPartitions(
            mounter.model.partitions, mounter.model.device)
    else:
        partitions = genPartitions([mounter.model], mounter.model.device)
    commands = concat(commands, mb.mountAll(partitions))

    return commands


def formatGen(formater):
    """
    Generate format commands from a parser.executor.format object
    """
    commands = ["\n#Formating partitions"]
    if type(formater.model) == type(parsemodel.disk()):
        partitions = genPartitions(
            formater.model.partitions, formater.model.device)
    else:
        partitions = genPartitions([formater.model], formater.model.device)
    for part in partitions:
        commands = concat(commands, pb.format(part))
    return commands


def PartitionTableGen(ptable):
    """
    Convert a partitiontable gen step to a list of commands
    """
    model = ptable.model
    table = tablemodel.disk(model.device, model.size,
                            genPartitions(model.partitions, model.device), model.gpt)
    return concat(["\n#Building partition table"], tablebuilder.buildPartitionTable(table))


def genPartitions(parserPartitions, diskdevice):
    """
    generate a list of model partition from a parser partition model
    """
    partitions = []
    # TODO: Generate logic volumes here as well
    for i, part in enumerate(parserPartitions):
        partitions.append(partition.partition(diskdevice+str(i+1),
                                              part.name, part.mount, part.filesystem, part.start, part.end, False))
    return partitions
