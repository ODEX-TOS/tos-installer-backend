import shell
import partitiontable
import config

class bootloader:
    def __init__(installcommand=config.BOOTLOADER_EFI, installDOSCommand=config.BOOTLOADER_DOS, configcommand=config.BOOTLOADER_CONFIG, partitiontype=partitiontable.EPartitionTabel.GPT):
        self.installcommand = installcommand
        self.installDOScommand = installDOScommand
        self.configcommand = configcommand
        self.partitiontype = partitiontype

    def install(self):
        if self..partitiontype == partitiontype.EPartitionTabel.GPT:
            shell.Command(self.installcommand.format(self.partitiontable.disk)).GetReturnCode()
        else:
             shell.Command(self.installDOScommand.format(self.partitiontable.disk)).GetReturnCode()
        return shell.Command(self.configcommand).GetReturnCode()
