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
