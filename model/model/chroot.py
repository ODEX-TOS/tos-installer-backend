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

    def start(self, command="/bin/bash", herefile="EOF"):
        if not type(command) is list:
            return [self.chroot.format(self.user, self.mountpoint) + " <<{}\n".format(herefile) + command + "\n" + herefile]
        commands = ""
        for item in command:
            commands += item + "\n"
        return [self.chroot.format(self.user, self.mountpoint) + " <<{}\n".format(herefile) + commands + "\n" + herefile]
