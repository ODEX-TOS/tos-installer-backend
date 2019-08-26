import packages
import shell
import config

class git:
    # Download a git url to a destination directory
    def __init__(self, url, destination):
        self.InstallGit()
        self.url = url
        self.destination = destination

    def init(self):
        shell.Command("git clone {} {}".format(self.url, self.destination))

    def InstallGit(self):
        installer = packages.Installer(packages=[config.GITPACKAGE])
        Installer.exec()
