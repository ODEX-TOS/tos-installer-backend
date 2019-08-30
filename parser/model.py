
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


class disk:
    """
    A disk object inside the model.disks of the yaml file
    """

    def __init__(self):
        self.device = None
        self.size = None
        self.gpt = True
        self.partitions = [None]


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


class chrootmodel:
    """
    A class as defined in the chroot part of the model.
    """

    def __init__(self):
        self.user = None
        self.mountpoint = "/mnt"


class user:
    """
    A class as defined in the user part of the model.
    """

    def __init__(self):
        self.name = None
        self.password = None
        self.shell = "/bin/bash"
        self.groups = None


class bootloader:
    """
    A class as defined in the bootloader part of the model.
    """

    def __init__(self):
        self.device = None


class system:
    """
    A class as defined in the chroot part of the model.
    """

    def __init__(self):
        self.local = None
        self.keymap = None
        self.hostname = None
        self.password = None


class package:
    """
    A class as defined in the packages part of the model.
    """

    def __init__(self):
        self.name = None
        self.file = None
        self.packages = None


class script:
    """
    A class as defined in the script part of the model.
    It contains a script data
    """

    def __init__(self):
        self.name = None
        self.file = None
        self.command = None


def generateModel(raw):
    """
    generate a model from a raw yaml model
    """
    representation = models()
    for dic in raw:
        if exists(dic, "bootloader"):
            representation.bootloader = generateBootloader(dic["bootloader"])
        if exists(dic, "system"):
            representation.system = generateSystem(dic["system"])
        if exists(dic, "chroots") and type(dic["chroots"]) is list:
            representation.chroots = generateChroots(dic)
        if exists(dic, "disks") and type(dic["disks"]) is list:
            representation.disks = generateDisks(dic)
        if exists(dic, "packages") and type(dic["packages"]) is list:
            representation.packages = generatePackages(dic)
    return representation


def generateBootloader(raw):
    representation = bootloader()
    if exists(raw, "device"):
        representation.device = raw["device"]
    return representation


def generateDisks(raw):
    end = []
    for pack in raw["disks"]:
        representation = disk()
        if exists(pack, "device"):
            representation.device = pack["device"]
        if exists(pack, "size"):
            representation.size = pack["size"]
        if exists(pack, "gpt"):
            representation.gpt = pack["gpt"]
        if exists(pack, "partitions"):
            representation.partitions = generatePartitions(pack["partitions"])

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
        end.append(representation)
    return end


def generateSystem(raw):
    representation = system()
    if exists(raw, "hostname"):
        representation.hostname = raw["hostname"]
    if exists(raw, "keymap"):
        representation.keymap = raw["keymap"]
    if exists(raw, "local"):
        representation.local = raw["local"]
    if exists(raw, "password"):
        representation.password = raw["password"]

    return representation


def generatePackages(raw):
    end = []
    for pack in raw["packages"]:
        representation = package()
        if existsDoubleKey(pack, "package", "package"):
            representation.name = pack["package"]["package"]
        if existsDoubleKey(pack, "package", "packagefile"):
            representation.file = pack["package"]["packagefile"]
        end.append(representation)
    return end


def generateChroots(raw):
    end = []
    for pack in raw["chroots"]:
        representation = chrootmodel()
        if existsDoubleKey(pack, "chroot", "name"):
            representation.name = pack["chroot"]["name"]
        end.append(representation)
    return end


def generateUsers(raw):
    end = []
    for pack in raw["users"]:
        representation = user()
        if exists(pack, "name"):
            representation.name = pack["name"]
        if exists(pack, "password"):
            representation.password = pack["password"]
        if exists(pack, "shell"):
            representation.shell = pack["shell"]
        if exists(pack, "groups"):
            representation.groups = pack["groups"]
        end.append(representation)
    return end


def exists(dict, key):
    return key in dict.keys()


def existsDoubleKey(dict, key1, key2):
    return key1 in dict.keys() and key2 in dict[key1]
