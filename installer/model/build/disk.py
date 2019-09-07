from installer.model.model.disk import disk
import installer.model.build.partition as partition
import installer.config as config
import os
import sys
sys.path.append("...")  # set all imports to root imports


def buildPartitionTable(Disk):
    """
    Generate the partition table commands based on a disk object
    The disk object must have a root partition
    """
    commands = [getPartitionTableType(Disk)]

    for part in Disk.partitions:
        commands = concat(commands, getPartitionCommands(
            Disk, part, part.offset))
    return commands


def buildPartitionTableEntries(Disk):
    """
    Generate the partition table commands based on a disk object
    It appends the partitions to an exisiting partition table
    """
    commands = []

    for index, part in enumerate(Disk.partitions):
        commands = concat(commands, getPartitionCommands(
            Disk, part, part.offset))
    return commands


def getPartitionCommands(Disk, part, index):
    if part.mountpoint == "[SWAP]" or part.mountpoint == "swap":
        return partition.buildSwapPartition(Disk, part, index, part.name)
    elif part.bIsEncrypted:
        return partition.buildEncryptedPrimaryPartition(Disk, part, index, part.name)
    elif part.mountpoint == "/boot/efi" and Disk.bIsGPT:
        return partition.buildBootablePartition(Disk, part, index, part.name, Disk.bIsGPT)
    elif part.mountpoint == "/boot" and not Disk.bIsGPT:
        return partition.buildBootablePartition(Disk, part, index, part.name, Disk.bIsGPT)
    elif part.resize:
        return partition.buildResizePartition(Disk, part, index, part.name)
    return partition.buildPrimaryPartition(Disk, part, index, part.name)


def concat(list1, list2):
    newlist = list1
    for item in list2:
        newlist.append(item)
    return newlist


def getPartitionTableType(Disk):
    if Disk.bIsGPT:
        return partition.getBaseCommand(Disk) + "mklabel gpt"
    return partition.getBaseCommand(Disk) + "mklabel msdos"