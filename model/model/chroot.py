import config
import shell
import os
import sys
sys.path.append("...")  # set all imports to root imports


class chroot:
    def __init__(self, chrootfunc=config.CHROOT, mountpoint="/mnt", user="root"):
        self.chroot = chrootfunc
        self.mountpoint = mountpoint
        self.user = user

    def start(self, command="/bin/bash"):
        return shell.Command(self.chroot.format(self.user, self.mountpoint, command)).GetReturnCode()
