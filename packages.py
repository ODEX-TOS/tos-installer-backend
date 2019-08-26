import shell
import config

# Class to manage how to install softwate
class Installer:
    # packages should be a list of strings
    def __init__(basecommand=config.INSTALLCOMMAND, packages=""):
        self.base = basecommand
        self.packages = packages

    # try to install packages. Returns the status code after installation
    def exec(self):
        packagelist = ""
        for package in self.packages:
            packagelist += package + " "
        obj=shell.Command(self.basecommand + " " + packagelist)
        return obj.GetReturnCode()

    def ExecFromFile (self, filename):
        with open('filename') as f:
                lines = f.read().splitlines()
        self.packages = lines
        return self.exec()


# This is a class that is only related to arch based distro's Since it uses the AUR community repo
# Dependecies should be a file containing the packages in a list
class AURHandler:
    def __init__(dependencyFile="", url=config.AURHELPER, directory=config.AURHELPERDIR):
        self.url = url
        self.dir = directory
        self.dependencyFile = dependencyFile

    def InstallDep(self):
        if self.dependencyFile != "":
            installer = Installer()
            installer.ExecFromFile(self.dependencyFile)

        
    def build(self):
        self.InstallDep()
        obj=shell.Command("""
        cd
        git clone {}
        cd {}
        yes | makepkg -si
        cd
        rm -rf {}
        """.format(self.url, self.dir, self.dir))
        return obj.GetReturnCode()

