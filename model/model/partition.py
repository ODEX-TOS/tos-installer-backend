class partition:
    """
    Stores general information about partitions
    """

    def __init__(self, device=None, mountpoint=None, filesystem=None, start=None, end=None):
        """
        @device is the device of the partition eg /dev/sda1 or /dev/nvme1p1
        @mountpoint is the location to which the partition is mounted eg /boot or /
        @filesystem is a value of EFilesystem
        @start is a parted value at which point the partition starts on the disk
        @end is a parted value at which point the partition stops on the disk
        """
        self.device = device
        self.mountpoint = mountpoint
        self.filesystem = filesystem
        self.start = start
        self.end = end


class EFilesystem:
    """
    A simple enumerator containing the different type of filesystems
    """
    EXT4 = "ext4"
    BTRFS = "btrfs"
    FAT32 = "fat32"
