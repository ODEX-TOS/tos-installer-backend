from installer.model.model import disk as model
from installer.model.gen import partition
import installer.shell as shell
import sys
sys.path.append("...")  # set all imports to root imports


def GetDiskSize(device):
    """
    Return the size of a disk
    """
    obj = shell.Command("lsblk {}".format(device) +
                        " -s --noheading | awk '{print $4}'")
    return obj.GetStdout()


def getPartitionsByDisk(device):
    """
    Generate all partitions found on a disk
    """
    # Gets a list of partitions based on file location
    obj = shell.Command("lsblk " + device + " --noheading -p --list | grep -E '" +
                        device + "[a-zA-Z0-9]+' | awk '{print $1}'")
    parts = obj.GetStdout().split()

    # convert the list of string into partition objects
    partitions = []
    for part in parts:
        partitions.append(partition.getPartitionByDevice(part))
    return partitions


def getAllDisks():
    """
    Return all disks found in /dev
    """
    obj = shell.Command(
        "fdisk -l | grep -E 'Disk /dev' | awk '{print $2}' | sed 's/://'")
    diskslist = obj.GetStdout().split()

    disks = []
    for disk in diskslist:
        disks.append(model.disk(disk, GetDiskSize(
            disk), getPartitionsByDisk(disk)))
    return disks
