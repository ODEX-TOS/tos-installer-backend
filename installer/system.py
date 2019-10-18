
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
import installer.shell as shell
import installer.config as config
import installer.model.build.software as swb
import installer.model.model.software as sw
# TODO: add localtime generator
# shell command is as followed ln -sf /usr/share/zoneinfo/"$continent"/"$capital" /etc/localtime
# where $continent is in  /usr/share/zoneinfo/*
# where $capital is in /usr/share/continent/*


class system:
    def __init__(self, locale=config.LOCALE, keymap=config.KEYMAP, hostname=config.HOSTNAME, password_root=config.ROOT_PWD):
        self.locale = locale
        self.keymap = keymap
        self.hostname = hostname
        self.password_root = password_root

    def setup(self, config):
        commands = [
            "timedatectl set-ntp true",
            "hwclock --systohc",
            "sed -i 's:^#.*{}:{}:' /etc/locale.gen".format(
                self.locale, self.locale),
            "locale-gen",
            "echo 'LANG={}' > /etc/locale.conf".format(self.locale),
            "echo KEYMAP='{}' > /etc/vconsole.conf".format(self.keymap),
            "echo '{}' > /etc/hostname".format(self.hostname),
            "echo -e '127.0.0.1   localhost\n::1      localhost\n127.0.1.1    {}.localdomain  {}' > /etc/hosts".format(
                self.hostname, self.hostname),
            "echo 'root:{}' | chpasswd".format(self.password_root),
            "echo '%wheel ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers",
        ]
        # installing kernel
        commands = concat(commands, swb.installSoftware(sw.software(
            config["INSTALLCOMMAND"], packages=config["KERNEL"])))
        return commands


def concat(list1, list2):
    newList = list1
    for item in list2:
        newList.append(item)
    return newList

# TODO: return all locals


def getAllLocals():
    return

# TODO: return all keymaps


def getAllKeyMaps():
    return
