import config
import os
import sys
sys.path.append("...")  # set all imports to root imports


class software:
    """
    A object holding all the data needed to be installable
    """

    def __init__(self, installer=config.INSTALLCOMMAND, packages=[]):
        """
        @installer = the command to install software
        @packages = all the packages that should be installed
        """
        self.installer = installer
        self.packages = packages
