class disk:
    """
    A basic class demonstrating all information of a disk
    """

    def __init__(self, device=None, size=None, partitions=None):
        """
        @device = location in the filesystem of the device eg /dev/sda
        @size = the size in bytes/kilobytes/megabytes,Gigabytes eg 1.1G or 1.8TB
        @ partitions = a list of partition (model/model/partition)
        """
        self.device = device
        self.size = size
        self.partitions = partitions
