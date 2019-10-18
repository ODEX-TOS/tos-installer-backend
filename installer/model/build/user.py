
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


def listToString(list, delimiter=","):
    string = ""
    for item in list:
        string += item + delimiter
    # return the full string except the last delimiter since it doesn't delimit
    # eg 1,2,3,4,
    # to 1,2,3,4
    return string[:-1]


def getEncryptedPassword(password):
    return crypt.crypt(password, "password")
