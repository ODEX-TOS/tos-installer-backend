
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
class disk:
    """
    A basic class demonstrating all information of a disk
    """

    def __init__(self, device=None, size=None, partitions=None, bIsGPT=True):
        """
        @device = location in the filesystem of the device eg /dev/sda
        @size = the size in bytes/kilobytes/megabytes,Gigabytes eg 1.1G or 1.8TB
        @ partitions = a list of partition (model/model/partition)
        @bIsGPT = tells us if the partition table if GPT or not
        """
        self.device = device
        self.size = size
        self.partitions = partitions
        self.bIsGPT = bIsGPT

    def toString(self, indent=""):
        partstr = ""
        if self.partitions != None:
            for part in self.partitions:
                partstr += part.toString() + "\n"
            return "{}Disk {} : Size {}".format(indent, self.device, self.size) + " Partitions {\n" + partstr + " }"
        else:
            return "{}Disk {} : Size {} ".format(indent, self.device, self.size)
