import shell

# Generate a filesystem on a partition
class filesystem:
    def __init__(self, partition):
        self.partition = partition

    def makefs():
        shell.Command("mkfs.ext4 {}".format(self.partition.disk+self.partition.partition)).GetReturnCode()

# Create an ext4 filesystem on your partition
class ext4(filesystem):
    def __init__(self, partition):
        super(partition)

# Create a fat32 filesystem on your partition
class fat32(filesystem):
    def __init__(self, partition):
        super(partition)

    def makefs():
        shell.Command("mkfs.fat -F32 {}".format(self.partition.disk+self.partition.partition)).GetReturnCode()


# Create a btrfs filesystem on your partitions
class btrfs(filesystem):
    def __init__(self, partition):
        super(partition)

    def makefs():
        shell.Command("mkfs.btrfs {}".format(self.partition.disk+self.partition.partition)).GetReturnCode()

# Return a filesystem object based on the type of the partition
def CreateFilesystem(partition):
    if partition.type == "ext4":
        return ext4(partition)
    if partition.type == "btrfs":
        return btrfs(partition)
    if partition.type == "fat32":
        return fat32(partition)
    return filesystem(partition)
