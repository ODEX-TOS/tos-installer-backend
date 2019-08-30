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
import model.model.script as script


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
            command = concat(commands, chrootGen(step))
        else:
            print(step)
    return commands

# TODO: implement recursive chroot step generator


def chrootGen(step):
    """
    Build chroot command from a parser.executor.chroot object
    """
    return []


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
