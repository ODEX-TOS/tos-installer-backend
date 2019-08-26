import shell

# Wrapper for a chrooting utility 
class chroot:
    def __init__(self, chrootcommand="arch-chroot -u {} {} {}", mountpoint="/mnt", user="root"):
        self.chroot = chrootcommand
        self.mountpoint = mountpoint
        self.bIsRoot = bIsRoot
        self.user=user
    # Command to run in the chrooted environment
    def start(self, command="/bin/bash"):
        return shell.Command(chrootcommand.format(self.user, self.mountpoint, command)).GetReturnCode()
