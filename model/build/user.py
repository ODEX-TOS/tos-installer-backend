import crypt
import os
import sys
sys.path.append("...")  # set all imports to root imports


def makeUnixUser(user, config):
    """
    return a list of commands needed to build the user
    """
    groups = listToString(user.groups)
    return [config["USERADD"].format(getEncryptedPassword(user.password), groups, user.shell, user.name)]


def listToString(list, delimiter=" "):
    string = ""
    for item in list:
        string += item + delimiter
    # return the full string except the last delimiter since it doesn't delimit
    # eg 1,2,3,4,
    # to 1,2,3,4
    return string[:-1]


def getEncryptedPassword(password):
    return crypt.crypt(password, "password")
