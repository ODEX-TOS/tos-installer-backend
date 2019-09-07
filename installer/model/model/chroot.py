import installer.config as config
import installer.shell as shell
import os
import sys
sys.path.append("...")  # set all imports to root imports


class chroot:
    def __init__(self, chrootfunc=config.CHROOT, mountpoint="/mnt", user="root"):
        self.chroot = chrootfunc
        self.mountpoint = mountpoint
        self.user = user

    def start(self, command="/bin/bash", herefile="EOF"):
        """
        Generate the chrooted environment commands. A chrooted environment should have a list of commands to execute (inside of this)
        A herefile/string should be supplied to specify the delimiter as the underlying structure uses these. 
        The herestring should be a string of charachters that is not presend inside the command
        """
        if self.user == "root":
            return self.chrootAsRoot(command, herefile)
        return self.chrootAsUser(command, herefile, herefile+"2")

    def chrootAsUser(self, command, herefile, userHerefile):
        """
        This is an internal method and should not be used outside the scope of this class
        Use start instead
        """
        if not type(command) is list:
            return [self.chroot.format("root", self.mountpoint) + " <<{}\n".format(herefile) + "su {} <<\{}\n".format(self.user, userHerefile) + command.replace("$", "\\$") + "\n" + userHerefile + "\n" + herefile]
        commands = ""
        for item in command:
            commands += item + "\n"
        return [self.chroot.format("root", self.mountpoint) + " <<{}\n".format(herefile) + "su {} <<\{}\n".format(self.user, userHerefile) + commands.replace("$", "\\$") + "\n" + userHerefile + "\n" + herefile]

    def chrootAsRoot(self, command, herefile):
        """
        This is an internal method and should not be used outside the scope of this class
        Use start instead
        """
        if not type(command) is list:
            return [self.chroot.format(self.user, self.mountpoint) + " <<{}\n".format(herefile) + command.replace("$", "\\$") + "\n" + herefile]
        commands = ""
        for item in command:
            commands += item + "\n"
        return [self.chroot.format(self.user, self.mountpoint) + " <<{}\n".format(herefile) + commands.replace("$", "\\$") + "\n" + herefile]
