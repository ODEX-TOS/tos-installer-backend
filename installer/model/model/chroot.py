
# MIT License
# 
# Copyright (c) 2019 Meyers Tom
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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
