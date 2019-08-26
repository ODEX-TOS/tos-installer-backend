import shell



#Stores the data of 1 single partition
class Partition:
    def __init__(self, disk, partition):
        self.partition = partition
        self.disk = disk
        self.size = self.GetSize()
        self.mountpoint = self.GetMountPoint()
        self.type= self.GetType()

    def GetSize(self):
        obj=shell.Command("lsblk {} --noheading".format(self.disk+self.partition) + "| awk '{print $4}'")
        return obj.GetStdout()

    def GetMountPoint(self):
        obj=shell.Command("lsblk {} --noheading".format(self.disk+self.partition) + "| awk '{print $7}'")
        result = obj.GetStdout()
        if result == " ":
            return None
        return result

    def GetType(self):
        #obj=shell.Command("df -T -P " + self.partition + " | tail -n1 | awk '{print $2}'")
        obj=shell.Command("lsblk --fs --noheadings --lis -p " + self.disk+self.partition + " | awk '{print $2}' | head -n1")
        return obj.GetStdout()

    def toString(self):
        return "Partition {} (Size: {}, Mount: {}, filesystem: {})".format(self.disk + self.partition,self.size,self.mountpoint, self.type)
