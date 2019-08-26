import shell
import partition


# Store a single disk as an object
class Disk:
    # disk is a string pointing to the disk file
    # partitions is an array of partititons
    def __init__(self, disk, partitions):
        self.disk = disk
        self.partitions=partitions
        self.size = self.GetSize()

    def GetSize(self):
        obj=shell.Command("lsblk {}".format(self.disk) + " -s --noheading | awk '{print $4}'")
        return obj.GetStdout()

    def toString(self):
        partstr=""
        if self.partitions != None:
            for part in self.partitions:
                partstr += "\t" + part.toString() + "\n"
            return "Disk {} : Size {}".format(self.disk, self.size) + " Partitions {\n" + partstr + " }"
        else:
            return "Disk {} : Size {} ".format(self.disk, self.size)


# return a list of partition objects
def getPartitionsByDisk(disk):
    # Gets a list of partitions based on file location
    obj=shell.Command("lsblk " + disk + " --noheading -p --list | grep -E '"+ disk +"[a-zA-Z0-9]+' | awk '{print $1}'")
    parts=obj.GetStdout().split()

    # convert the list of string into partition objects
    partitions = []
    for part in parts:
        partitions.append(partition.Partition(disk, part.replace(disk,"")))
    return partitions

# return a list of disk objects
def getAllDisks():
    obj=shell.Command("fdisk -l | grep -E 'Disk /dev' | awk '{print $2}' | sed 's/://'")
    diskslist=obj.GetStdout().split()

    disks = []
    for disk in diskslist:
        disks.append(Disk(disk, getPartitionsByDisk(disk)))
    return disks
        



