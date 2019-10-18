
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


def handleEncryptedPartition(part, config):
    """
    Convert a partition into a luks volume
    The volume is created from @volumes
    @volumes = a list of logicvolumes mounted on config.LUKS_DEVICE
    The important parameters of @volumes is the mountpoint, name and size
    """
    command = ["modprobe dm-crypt", "modprobe dm-mod"]
    command.append("printf '{}' | ".format(part.password) +
                   config["LUKS"].format(part.device))
    command.append("printf '{}' | ".format(part.password) +
                   config["LUKS_OPEN"].format(part.device))
    command.append("pvcreate " + config["LUKS_DEVICE"])
    command.append("vgcreate {} ".format(
        config["LUKS_NAME"]) + config["LUKS_DEVICE"])
    for volume in part.volumes:
        command.append(
            "lvcreate -n {} -L {} {}".format(volume.name, volume.size, config["LUKS_NAME"]))
    # add format command for volumes
    for volume in part.volumes:
        formating = formatVolume(volume.name, volume.mountpoint, config)
        for form in formating:
            command.append(form)
    return command


# TODO: make it possible to format different filesystems


def formatVolume(name, mountpoint, config):
    return ["mkfs.ext4 -F -L {} {}".format(name, "/dev/mapper/{}-{}".format(config["LUKS_NAME"], name))]
