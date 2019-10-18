
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
import installer.model.model.software as sw
import installer.model.build.software as builder
import installer.shell
import os
import sys
sys.path.append("...")  # set all imports to root imports


class script:
    """
    A class containing data for running a shell script
    """

    def __init__(self, shell="/bin/sh", payload="echo payload", user="root"):
        """
        @shell the shell that is running this very script
        @payload the commands that the shell will be running
        @user the user that is going to run this shell script
        """
        self.shell = shell
        self.payload = payload
        self.user = user

    def exec(self):
        return [self.shell + " " + self.payload]


class bootloader:
    """
    Object holding all information for writing a bootloader to a boot partition
    """

    def __init__(self, shell="/bin/sh -c", device="/dev/sda", installcommand=config.BOOTLOADER_EFI, installDOSCommand=config.BOOTLOADER_DOS, configcommand=config.BOOTLOADER_CONFIG, bIsGPT=True, bIsEncrypted=False, kernel="linux", partitionDevice="/dev/sda1"):
        self.shell = shell
        self.installCommand = installcommand
        self.installDOSCommand = installDOSCommand
        self.configCommand = configcommand
        self.bIsGPT = bIsGPT
        self.device = device
        self.bIsEncrypted = bIsEncrypted
        self.kernel = kernel
        self.partitionDevice = partitionDevice

    def exec(self):
        """
        Write a bootloader to the boot partition
        """
        commands = []
        if self.bIsEncrypted:
            commands.append(
                self.shell + "sed -i 's:HOOKS=(\(.*\)):HOOKS=(\\1 encrypt lvm2):' /etc/mkinitcpio.conf")
            commands.append(
                'sed -i "s;^GRUB_CMDLINE_LINUX_DEFAULT=.*;GRUB_CMDLINE_LINUX_DEFAULT=\\"quiet cryptdevice={}:luks_lvm\\";" /etc/default/grub'.format(self.partitionDevice))
            commands.append(
                'sed -i "s/^#GRUB_ENABLE_CRYPTODISK=y/GRUB_ENABLE_CRYPTODISK=y/" /etc/default/grub'
            )
        commands.append(
            self.shell + "mkinitcpio -p {}".format(self.kernel[0]))
        if self.bIsGPT:
            commands.append(
                self.shell + "{}".format(self.installCommand).format(self.device))
        else:
            commands.append(
                self.shell + "{}".format(self.installDOSCommand).format(self.device))
        commands.append(self.shell + "{}".format(self.configCommand))
        return commands


class git(script):
    """
    A simple abstraction ontop of the script class.
    It handles installing git packages
    """

    def __init__(self, url, directory):
        self.url
        self.directory

    def install(self):
        """
        Install a git repository to a specific location. It also installs git in case that is not present
        return the status code from git.
        If installing git fails it returns None
        """
        return [self.installGit(), "git clone {} {}".format(self.url, self.destination)]

    def installGit(self):
        """
        Install git if it doesn't exist yes
        """
        software = sw.software(packages=[config.GITPACKAGE])
        return builder.installSoftware(software)
