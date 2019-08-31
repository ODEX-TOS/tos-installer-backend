from model.model.partition import partition, EFilesystem
import config
import shell
import os
import sys
sys.path.append("...")  # set all imports to root imports


def handleEncryptedPartition(part, config):
    """
    Convert a partition into a luks volume
    The volume is created from @volumes
    @volumes = a list of logicvolumes mounted on config.LUKS_DEVICE
    The important parameters of @volumes is the mountpoint, name and size
    """
    command = ["modprobe dm-crypt", "modprobe dm-mod"]
    command.append(config["LUKS"].format(part.device))
    command.append(config["LUKS_OPEN"].format(part.device))
    command.append("pvcreate " + config["LUKS_DEVICE"])
    command.append("vgcreate " + config["LUKS_DEVICE"])
    for volume in part.volumes:
        command.append(
            "lvcreate -n {} -L {} {}".format(volume.name, volume.size, config["LUKS_NAME"]))
    # add format command for volumes
    for volume in part.volumes:
        command.append(formatVolume(volume.name, volume.mountpoint, config))
    return command


# TODO: make it possible to format different filesystems


def formatVolume(name, mountpoint, config):
    return "mkfs.ext4 -L {} {}".format(name, "/dev/mapper/{}-{}".format(config["LUKS_NAME"], name))
