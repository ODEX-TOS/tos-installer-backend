import shell

# Enum used to indicate the partitiontable
class EPartitionTabel:
    GPT = "gpt"
    MSDOS = "msdos"


# Class that stores information needed to generate a partitiontable
class PartitionInfo:
    def __init__(self, name, bIsBootable, start, end, bIsEncrypted, bIsSwap):
        self.name = name
        self.bIsBootable = bIsBootable
        self.start = start
        self.end = end
        self.bIsEncrypted = bIsEncrypted
        self.bIsSwap = bIsSwap

# Class that stores a generatable partitiontable
class PartitionTable:
    
    def __init__(self, tabletype, disk, listPartitions):
        self.type=tabletype
        self.disk = disk
        self.partitions = listPartitions

    def getBaseCommand(self):
        return "parted --script '{}' ".format(self.disk)

    def setBootable(self, partition):
        if self.type == EPartitionTabel.GPT:
            return "mkpart ESP fat32 {} {}".format(partition.start, partition.end)
        
        return "mkpart primary {} {}".format(partition.start, partition.end)

    def generateCommand(self):
        commands = []
        commands.append(self.getBaseCommand() + "'mklabel {}'".format(self.type))
        i=1 
        for partition in self.partitions:
            
            if partition.bIsBootable:
                commands.append(self.getBaseCommand() + self.setBootable(partition))
                commands.append(self.getBaseCommand() + "set {} boot on".format(i))
            
            elif partition.bIsEncrypted:
                commands.append(self.getBaseCommand() + "mkpart primary {} {}".format(partition.start, partition.end))
                commands.append(self.getBaseCommand() + "set {} lvm on".format(i))
            else:
                commands.append(self.getBaseCommand() + "mkpart primary {} {}".format(partition.start, partition.end))

            commands.append(self.getBaseCommand() + "name {} {}".format(i, partition.name))
            i+=1
        return commands


def GenerateDefaultEncryptedTable(disk, tabletype):
    parts = []
    if tabletype == EPartitionTabel.GPT:
        parts.append(PartitionInfo("efi", True, "1MiB", "200MiB", False, False))
        parts.append(PartitionInfo("boot", False, "200MiB", "800MiB", False, False))
        parts.append(PartitionInfo("lvm", False, "800MiB", "100%", True, False))
    elif tabletype == EPartitionTabel.MSDOS:
        parts.append(PartitionInfo("boot", True, "1MiB", "200MiB", False, False))
        parts.append(PartitionInfo("lvm", False, "800MiB", "100%", True, False))
    return PartitionTable(tabletype, disk, parts)

def GenerateDefaultTable(disk, tabletype):
    parts = []
    if tabletype == EPartitionTabel.GPT:
        parts.append(PartitionInfo("efi", True, "1MiB", "200MiB", False))
        parts.append(PartitionInfo("boot", False, "200MiB", "800MiB", False))
        parts.append(PartitionInfo("root", False, "800MiB", "100%", False))
    elif tabletype == EPartitionTabel.MSDOS:
        parts.append(PartitionInfo("boot", True, "1MiB", "200MiB", False))
        parts.append(PartitionInfo("root", False, "800MiB", "100%", False))
    return PartitionTable(tabletype, disk, parts)
