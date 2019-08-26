import partitiontable as pt
import shell
import config
import disk

# Mount partitions to a mountpoint
class Mounter:
    def __init__(self, Disk, mountpoint=config.MOUNTPOINT):
        self.mountpoint = mountpoint
        self.partitions = disk.getPartitionsByDisk(Disk)

    # Mount all partitions
    def mountAll(self):
        self.mountswap()
        self.mountroot()
        self.mountRest()

    # mount swap
    def mountswap(self):
        for partition in self.partitions:
            if partition.type == "swap":
                shell.Command("swapon {}; swapon -a; swapon -s".format(partition.disk+partition.partition)).GetReturnCode()

    # mount root parttion
    def mountroot(self):
        for partition in self.partitions:
            if partition.mountpoint == "/":
                shell.Command("mount {} {}".format(partition.disk+partition.partition, self.mountpoint))


    # mount anything except the root and swap partitions
    def mountRest(self):
        for partition in self.partitions:
            if partition.mountpoint == "/" or partition.type == "swap":
                continue
            shell.Command("mkdir -p {}".format(self.mountpoint+"/"+partition.mountpoint))
            shell.Command("mount {} {}".format(partition.disk+partition.partition,self.mountpoint+"/"+partition.mountpoint))
        

