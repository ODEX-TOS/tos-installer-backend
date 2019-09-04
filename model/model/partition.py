class partition:
    """
    Stores general information about partitions
    """

    def __init__(self, device=None, name="root", mountpoint=None, filesystem=None, start=None, end=None, bIsEncrypted=False, volumes=[], password="", resize=False, size=None, offset=0):
        """
        @device is the device of the partition eg /dev/sda1 or /dev/nvme1p1
        @name is the canoncial name for the partition
        @mountpoint is the location to which the partition is mounted eg /boot or /
        @filesystem is a value of EFilesystem
        @start is a parted value at which point the partition starts on the disk
        @end is a parted value at which point the partition stops on the disk
        @bIsEncrypted tells us if the partition should be encrypted
        @volumes: logic volumes that are hosted in this partition
        @password: the password for the encrypted drive
        @resize: A boolean telling us if the partition already exists and if we need to resize it. By default we don't
        @size: This is the size in string format as defined by parted. The isze will be the new partition size of the disk if size is provided start and end options don't matter anymore
        @offset: If the partitionindex is different than the ordered list that the parttion is defined in
        """
        self.device = device
        self.name = name
        self.mountpoint = mountpoint
        self.filesystem = filesystem
        self.start = start
        self.end = end
        self.bIsEncrypted = bIsEncrypted
        self.volumes = volumes
        self.password = password
        self.resize = resize
        self.size = size
        self.offset = str(offset)

    def toString(self, indent="\t"):
        return "\t partition: {} - mounted on {} as {} from {} to {}".format(self.device,
                                                                             self.mountpoint, self.filesystem, self.start, self.end)


class logicvolume:
    def __init__(self, name, size, mountpoint):
        self.name = name
        self.size = size
        self.mountpoint = mountpoint


class EFilesystem:
    """
    A simple enumerator containing the different type of filesystems
    """
    EXT4 = "ext4"
    BTRFS = "btrfs"
    FAT32 = "fat32"
    SWAP = "swap"
    LUKS = "luks"
