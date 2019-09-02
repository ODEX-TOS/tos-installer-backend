from model.model.partition import partition, EFilesystem
import config
import shell
import os
import sys
sys.path.append("...")  # set all imports to root imports


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
    # Add all other mounts
    for part in parts:
        if part.mountpoint != "/":
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
