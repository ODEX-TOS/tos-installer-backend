
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
from installer.model.model import partition
import installer.shell as shell
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
