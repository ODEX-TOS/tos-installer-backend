from model.model.software import software
import config
import shell
import os
import sys
sys.path.append("...")  # set all imports to root imports


def installSoftware(software):
    """
    Install arbitrary software based on a software object
    """
    packagelist = ""
    for package in software.packages:
        packagelist += package + " "
        obj = shell.Command(software.installer + " " + packagelist)
    return obj.GetReturnCode()


def BuildSoftwareFromFile(file, installer=config.INSTALLCOMMAND):
    """
    Build a software object from a file containing packages
    @file = a file containing packages (every line is a package)
    @installer = the base install command to install software
    """
    sw = software(basecommand=installer)
    with open('filename') as f:
        lines = f.read().splitlines()
    sw.packages = lines
    return sw
