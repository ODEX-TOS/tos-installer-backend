from model.model import partition
import shell
import sys
sys.path.append("...")  # set all imports to root imports


def getPartitionByDevice(device):
    size = shell.Command(
        "lsblk {} --noheading".format(device) + "| awk '{print $4}'").GetStdout()
    mount = shell.Command(
        "lsblk {} --noheading".format(device) + "| awk '{print $7}'").GetStdout()
    if mount == " ":
        mount = None
    filesystem = shell.Command("lsblk --fs --noheadings --lis -p " +
                               device + " | awk '{print $2}' | head -n1").GetStdout()
    return partition.partition(device, mount, filesystem, None, None)
