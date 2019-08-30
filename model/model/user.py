import config
import os
import sys
sys.path.append("...")  # set all imports to root imports


class user:
    """
    @name = the username of the user
    @password = the password in plain text
    @groups = a list of groups the user belongs to
    @shell = the default shell the users uses (absolute path eg /bin/bash)
    """

    def __init__(self, name, password, groups=config.GROUPS, shell=config.DEFAULT_SHELL):
        self.name = name
        self.password = password
        self.groups = groups
        self.shell = shell
