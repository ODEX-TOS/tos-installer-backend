
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
from installer.model.model.partition import partition, EFilesystem
import installer.config as config
import installer.shell as shell
import os
import sys
sys.path.append("...")  # set all imports to root imports

# TODO: mount all major partition mountpoint first eg mount / first then all /* second then all /*/* third etc. You cant mount /boot/efi for instance before mounting /boot
# currenly the mounting of /boot and /boot/efi are "hardcoded" but this should work for every arbitrary mountpoint


def mountAll(parts, mountpoint=config.MOUNTPOINT):
    """
    @parts= a list of partitions
    @mountpoint=the place to mount the partitions
    Mount a list of partitions in the right order
    First root is mounted then the rest
    Return a list of commands
    """
    command = []

    # Add the root mount first
    for part in parts:
        if part.mountpoint == "/":
            command = concat(command, mount(part, mountpoint))
            break
    # mount /boot as second (in case there is an efi directory the /boot should be mounted first)
    for part in parts:
        if part.mountpoint == "/boot":
            command = concat(command, mount(part, mountpoint))
    # Add all other mounts
    for part in parts:
        if part.mountpoint != "/" and part.mountpoint != "/boot":
            command = concat(command, mount(part, mountpoint))
    return command


def mount(part, mountpoint):
    """
    Mount a partition based on its filesystem/mountpoint
    """
    if part.mountpoint == "swap" or part.mountpoint == "[swap]":
        return mountswap(part, mountpoint)
    elif part.mountpoint == "/":
        return mountroot(part, mountpoint)
    return mountStandard(part, mountpoint)


def mountswap(part, mountpoint):
    """
    Mount a swap partition
    """
    return ["swapon {}".format(part.device), "swapon -a",  "swapon -s"]


def mountroot(part, mountpoint):
    """
    Mount the root partition
    """
    if not part.bIsEncrypted:
        return ["mount {} {}".format(part.device, mountpoint)]

    commands = []
    for volume in part.volumes:
        if volume.mountpoint == "/":
            commands.append("mount {} {}".format(
                "/dev/mapper/{}-{}".format(config.LUKS_NAME, volume.name), mountpoint + volume.mountpoint))
    for volume in part.volumes:
        if volume.mountpoint != "/":
            commands.append(
                "mkdir -p {}".format(mountpoint + volume.mountpoint))
            commands.append("mount {} {}".format(
                "/dev/mapper/{}-{}".format(config.LUKS_NAME, volume.name), mountpoint + volume.mountpoint))
    return commands


def mountStandard(part, mountpoint):
    """
    Mount all partitions that are not "special" aka partitions that are not root, swap etc
    boot partitions are allowed here
    """
    mount = mountpoint + "/" + part.mountpoint
    if mountpoint[-1:] == "/" or part.mountpoint[0] == "/":
        mount = mountpoint + part.mountpoint
    return ["mkdir -p {}".format(mount), "mount {} {}".format(part.device, mount)]


def concat(list1, list2):
    newList = list1
    for item in list2:
        newList.append(item)
    return newList
