import config
import model.model.software as sw
import model.build.software as builder
import shell
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


class bootloader:
    """
    Object holding all information for writing a bootloader to a boot partition
    """

    def __init__(self, shell="/bin/sh -c", device="/dev/sda", installcommand=config.BOOTLOADER_EFI, installDOSCommand=config.BOOTLOADER_DOS, configcommand=config.BOOTLOADER_CONFIG, bIsGPT=True):
        self.shell = shell
        self.installCommand = installcommand
        self.installDOSCommand = installDOSCommand
        self.configCommand = configcommand
        self.bIsGPT = bIsGPT
        self.device = device

    def exec(self):
        """
        Write a bootloader to the boot partition
        """
        commands = []
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
