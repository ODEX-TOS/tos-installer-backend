
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

# TODO: add logic volumes as a subtype of a partition


class models:
    """
    A class based representation of the model section of the yaml file
    """

    def __init__(self):
        self.disks = [None]
        self.bootloader = None
        self.system = None
        self.packages = [None]
        self.chroots = [None]
        self.users = [None]
        self.scripts = [None]
        self.network = None

    def __str__(self):
        return "model \n\tdisks: {}\n\tbootloader: {}\n\tsystem: {}\n\tpackages: {}\n\tchroots: {}\n\tusers: {}\n\tscripts: {}, \n\tnetwork: {}".format(self.disks, self.bootloader, self.system, self.packages, self.chroots, self.users, self.scripts, self.network)


class disk:
    """
    A disk object inside the model.disks of the yaml file
    """

    def __init__(self):
        self.device = None
        self.size = None
        self.gpt = True
        self.partitions = [None]
        self.bGenTable = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "\n\tdisk -- device: {} -- size: {} -- gpt: {} -- \n\t\tpartitions [ {} ]".format(self.device, self.size, self.gpt, self.partitions)


class partition:
    """
    A class representing a partition as defined in models.disks.partition
    """

    def __init__(self):
        self.name = None
        self.mount = None
        self.filesystem = None
        self.start = None
        self.end = None
        self.device = None
        self.bIsEncrypted = False
        self.password = ""  # the encryption password
        self.volumes = [None]
        self.offset = None
        self.resize = False
        self.size = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "\n\t\t\tpartition -- name: {} -- mount: {} -- filesystem: {} -- start: {} -- end: {} -- device: {} -- encrypted {} -- password {} -- volumes {}".format(self.name, self.mount, self.filesystem, self.start, self.end, self.device, self.bIsEncrypted, self.password, self.volumes)


class logicVolume:
    """
    A representation of logicvolumes inside a volumegroup
    """

    def __init__(self):
        self.name = None
        self.size = None
        self.mountpoint = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "\n\t\t\t\tlogic volume -- name: {} -- size: {} -- mountpoint: {}".format(self.name, self.size, self.mountpoint)


class chrootmodel:
    """
    A class as defined in the chroot part of the model.
    """

    def __init__(self, config):
        self.mountpoint = config["MOUNTPOINT"]
        self.name = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "\n\t\tchroot -- user: {} -- mountpount: {}".format(self.name, self.mountpoint)


class user:
    """
    A class as defined in the user part of the model.
    """

    def __init__(self, config):
        self.name = None
        self.password = None
        self.shell = config["DEFAULT_SHELL"]
        self.groups = config["GROUPS"]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "\n\t\tuser -- name: {} -- password: {} -- shell: {} -- groups: {}".format(self.name, self.password, self.shell, self.groups)


class bootloader:
    """
    A class as defined in the bootloader part of the model.
    """

    def __init__(self):
        self.device = None

    def __str__(self):
        return "device: {}".format(self.device)


class system:
    """
    A class as defined in the chroot part of the model.
    """

    def __init__(self, config):
        self.local = config["LOCAL"]
        self.keymap = config["KEYMAP"]
        self.hostname = config["HOSTNAME"]
        self.password = config["ROOT_PWD"]

    def __str__(self):
        return "local: {} -- keymap: {} -- hostname: {} -- password {}".format(self.local, self.keymap, self.hostname, self.password)


class package:
    """
    A class as defined in the packages part of the model.
    """

    def __init__(self, config):
        self.name = None
        self.file = None
        self.packages = None
        self.install = config["INSTALLCOMMAND"]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "\n\t\tpackage -- name: {} --install: {} -- file: {} -- packages: {}".format(self.name, self.install, self.file, self.packages)


class script:
    """
    A class as defined in the script part of the model.
    It contains a script data
    """

    def __init__(self):
        """
        if both file and command are set the file will be executed
        """
        self.name = None
        self.file = None  # run the file as a script
        self.command = None  # run a command as a script

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "script -- name: {} -- file: {} -- command: {}".format(self.name, self.file, self.command)


class network:
    """
    General information about your network
    """

    def __init__(self):
        self.ssid = None
        self.password = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "network -- ssid: {} -- password: {}".format(self.ssid, self.password)


def generateModel(raw, config):
    """
    generate a model from a raw yaml model
    """
    representation = models()
    for dic in raw:
        if exists(dic, "bootloader"):
            representation.bootloader = generateBootloader(dic["bootloader"])
        if exists(dic, "system"):
            representation.system = generateSystem(dic["system"], config)
        if exists(dic, "chroots") and type(dic["chroots"]) is list:
            representation.chroots = generateChroots(dic, config)
        if exists(dic, "disks") and type(dic["disks"]) is list:
            representation.disks = generateDisks(dic)
        if exists(dic, "packages") and type(dic["packages"]) is list:
            representation.packages = generatePackages(dic, config)
        if exists(dic, "users") and type(dic["users"]) is list:
            representation.users = generateUsers(dic, config)
        if exists(dic, "scripts") and type(dic["scripts"]) is list:
            representation.scripts = generateScripts(dic)
        if exists(dic, "network"):
            representation.network = generateNetwork(dic["network"])
    return representation


def generateNetwork(raw):
    representation = network()
    representation.ssid = raw["ssid"]
    representation.password = raw["password"]
    return representation


def generateScripts(raw):
    end = []
    for pack in raw["scripts"]:
        representation = script()
        if existsDoubleKey(pack, "script", "name"):
            representation.name = pack["script"]["name"]
        if existsDoubleKey(pack, "script", "file"):
            representation.file = pack["script"]["file"]
        if existsDoubleKey(pack, "script", "command"):
            representation.command = pack["script"]["command"]
        end.append(representation)
    return end


def generateBootloader(raw):
    representation = bootloader()
    if exists(raw, "device"):
        representation.device = raw["device"]
    return representation


def generateDisks(raw):
    end = []
    for pack in raw["disks"]:
        pack = pack["disk"]
        representation = disk()
        if exists(pack, "device"):
            representation.device = pack["device"]
        if exists(pack, "size"):
            representation.size = pack["size"]
        if exists(pack, "gpt"):
            representation.gpt = pack["gpt"]
        if exists(pack, "partitions"):
            representation.partitions = generatePartitions(pack["partitions"])
        if exists(pack, "table"):
            representation.bGenTable = pack["table"]

        end.append(representation)
    return end


def generatePartitions(raw):
    end = []
    for pack in raw:
        representation = partition()
        if existsDoubleKey(pack, "partition", "name"):
            representation.name = pack["partition"]["name"]
        if existsDoubleKey(pack, "partition", "mount"):
            representation.mount = pack["partition"]["mount"]
        if existsDoubleKey(pack, "partition", "filesystem"):
            representation.filesystem = pack["partition"]["filesystem"]
        if existsDoubleKey(pack, "partition", "start"):
            representation.start = pack["partition"]["start"]
        if existsDoubleKey(pack, "partition", "end"):
            representation.end = pack["partition"]["end"]
        if existsDoubleKey(pack, "partition", "encrypted"):
            representation.bIsEncrypted = pack["partition"]["encrypted"]
        if existsDoubleKey(pack, "partition", "password"):
            representation.password = pack["partition"]["password"]
        if existsDoubleKey(pack, "partition", "offset"):
            representation.offset = pack["partition"]["offset"]
        if existsDoubleKey(pack, "partition", "resize"):
            representation.resize = pack["partition"]["resize"]
        if existsDoubleKey(pack, "partition", "size"):
            representation.size = pack["partition"]["size"]
        if existsDoubleKey(pack, "partition", "logicvolumes"):
            representation.volumes = generateVolumes(
                pack["partition"]["logicvolumes"])
        end.append(representation)
    return end


def generateVolumes(raw):
    end = []
    for volume in raw:
        representation = logicVolume()
        representation.name = volume["volume"]["name"]
        representation.size = volume["volume"]["size"]
        representation.mountpoint = volume["volume"]["mountpoint"]
        end.append(representation)
    return end


def generateSystem(raw, config):
    representation = system(config)
    if exists(raw, "hostname"):
        representation.hostname = raw["hostname"]
    if exists(raw, "keymap"):
        representation.keymap = raw["keymap"]
    if exists(raw, "local"):
        representation.local = raw["local"]
    if exists(raw, "password"):
        representation.password = raw["password"]

    return representation


def generatePackages(raw, config):
    end = []
    for pack in raw["packages"]:
        representation = package(config)
        if existsDoubleKey(pack, "package", "package"):
            representation.packages = pack["package"]["package"]
        if existsDoubleKey(pack, "package", "packagefile"):
            representation.file = pack["package"]["packagefile"]
        if existsDoubleKey(pack, "package", "name"):
            representation.name = pack["package"]["name"]
        if existsDoubleKey(pack, "package", "install"):
            representation.install = pack["package"]["install"]
        end.append(representation)
    return end


def generateChroots(raw, config):
    end = []
    for pack in raw["chroots"]:
        representation = chrootmodel(config)
        if existsDoubleKey(pack, "chroot", "name"):
            representation.name = pack["chroot"]["name"]
        if existsDoubleKey(pack, "chroot", "mount"):
            representation.mountpoint = pack["chroot"]["mount"]
        end.append(representation)
    return end


def generateUsers(raw, config):
    end = []
    for pack in raw["users"]:
        representation = user(config)
        if existsDoubleKey(pack, "user", "name"):
            representation.name = pack["user"]["name"]
        if existsDoubleKey(pack, "user",  "password"):
            representation.password = pack["user"]["password"]
        if existsDoubleKey(pack, "user", "shell"):
            representation.shell = pack["user"]["shell"]
        if existsDoubleKey(pack, "user", "groups"):
            representation.groups = pack["user"]["groups"]
        end.append(representation)
    return end


def exists(dict, key):
    return key in dict.keys()


def existsDoubleKey(dict, key1, key2):
    return key1 in dict.keys() and key2 in dict[key1]
