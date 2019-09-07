from installer.model.model.partition import partition, EFilesystem
from installer.model.build.encryption import handleEncryptedPartition
import installer.config as config
import installer.shell as shell
import os
import sys
sys.path.append("...")  # set all imports to root imports


def buildPrimaryPartition(disk, Partition, index=0, name="root"):
    """
    Alter the partition table to include a primary typed partition on a certain disk
    @disk is the device to alter its partition table
    @Partition is the model of a partition
    @index is the index of the partition in the partition table
    @name is the name to assign this partition in the table
    """
    commands = []
    commands.append(getBaseCommand(
        disk) + "mkpart primary {} {}".format(Partition.start, Partition.end))
    commands.append(getBaseCommand(disk) + "name {} {}".format(index, name))
    return commands


def buildBootablePartition(disk, Partition, index=0, name="boot", bIsGPT=True):
    """
    Alter the partition table to include a primary typed partition on a certain disk
    @disk is the device to alter its partition table
    @Partition is the model of a partition
    @index is the index of the partition in the partition table
    @name is the name to assign this partition in the table
    @bIsGPT tells us if the partition table ig GPT, if it isn't a msdos boot partition will be generated
    """
    commands = []
    if bIsGPT:
        commands.append(getBaseCommand(
            disk) + "mkpart ESP fat32 {} {}".format(Partition.start, Partition.end))
    else:
        commands.append(getBaseCommand(
            disk) + "mkpart primary {} {}".format(Partition.start, Partition.end))

    commands.append(getBaseCommand(disk) + "set {} boot on".format(index))
    commands.append(getBaseCommand(disk) + "name {} {}".format(index, name))
    return commands


def buildSwapPartition(disk, Partition, index=0, name="swap"):
    """
    Alter the partition table to include a primary typed partition on a certain disk
    @disk is the device to alter its partition table
    @Partition is the model of a partition
    @index is the index of the partition in the partition table
    @name is the name to assign this partition in the table
    """
    return buildPrimaryPartition(disk, Partition, index, name)


def buildEncryptedPrimaryPartition(disk, Partition, index=0, name="root"):
    """
    Alter the partition table to include a primary typed partition on a certain disk
    @disk is the device to alter its partition table
    @Partition is the model of a partition
    @index is the index of the partition in the partition table
    @name is the name to assign this partition in the table
    """
    commands = []
    commands.append(getBaseCommand(
        disk) + "mkpart primary {} {}".format(Partition.start, Partition.end))
    commands.append(getBaseCommand(disk) + "set {} lvm on".format(index))
    commands.append(getBaseCommand(disk) + "name {} {}".format(index, name))
    return commands


def buildResizePartition(disk, Partition, index=0, name="root"):
    """
    Resize an exisiting partition to a new size based on its index and the size
    """
    commands = []
    commands.append(getBaseCommand(
        disk) + "resizepart {} {}".format(index, Partition.size))
    return commands


def getBaseCommand(disk):
    """
    returns the base of the parted command
    """
    return "parted --script '{}' ".format(disk.device)


def format(part, config):
    """
    format a partition based on the filesystem. 
    It returns a list of command to run
    If no matching filesystem was found we return None
    """
    if part.filesystem == EFilesystem.EXT4:
        return ["mkfs.ext4 -F {}".format(part.device)]
    elif part.filesystem == EFilesystem.BTRFS:
        return ["mkfs.btrfs -f {}".format(part.device)]
    elif part.filesystem == EFilesystem.FAT32:
        return ["mkfs.fat -I -F32 {}".format(part.device)]
    elif part.filesystem == EFilesystem.SWAP:
        return ["mkswap -f {}".format(part.device)]
    elif part.bIsEncrypted or part.filesystem == EFilesystem.LUKS:
        return handleEncryptedPartition(part, config)
    return None
