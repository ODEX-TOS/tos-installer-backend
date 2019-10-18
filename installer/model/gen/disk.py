
# MIT License
# 
# Copyright (c) 2019 Meyers Tom
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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
