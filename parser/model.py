
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

    def __str__(self):
        return "model \n\tdisks: {}\n\tbootloader: {}\n\tsystem: {}\n\tpackages: {}\n\tchroots: {}\n\tusers: {}\n\tscripts: {}".format(self.disks, self.bootloader, self.system, self.packages, self.chroots, self.users, self.scripts)


class disk:
    """
    A disk object inside the model.disks of the yaml file
    """

    def __init__(self):
        self.device = None
        self.size = None
        self.gpt = True
        self.partitions = [None]

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

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "\n\t\t\tpartition -- name: {} -- mount: {} -- filesystem: {} -- start: {} -- end: {}".format(self.name, self.mount, self.filesystem, self.start, self.end)


class chrootmodel:
    """
    A class as defined in the chroot part of the model.
    """

    def __init__(self):
        self.mountpoint = "/mnt"
        self.name = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "\n\t\tchroot -- user: {} -- mountpount: {}".format(self.name, self.mountpoint)


class user:
    """
    A class as defined in the user part of the model.
    """

    def __init__(self):
        self.name = None
        self.password = None
        self.shell = "/bin/bash"
        self.groups = None

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

    def __init__(self):
        self.local = None
        self.keymap = None
        self.hostname = None
        self.password = None

    def __str__(self):
        return "local: {} -- keymap: {} -- hostname: {} -- password {}".format(self.local, self.keymap, self.hostname, self.password)


class package:
    """
    A class as defined in the packages part of the model.
    """

    def __init__(self):
        self.name = None
        self.file = None
        self.packages = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "\n\t\tpackage -- name: {} -- file: {} -- packages: {}".format(self.name, self.file, self.packages)


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
        if exists(dic, "users") and type(dic["users"]) is list:
            representation.users = generateUsers(dic)
        if exists(dic, "scripts") and type(dic["scripts"]) is list:
            representation.scripts = generateScripts(dic)
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
            representation.packages = pack["package"]["package"]
        if existsDoubleKey(pack, "package", "packagefile"):
            representation.file = pack["package"]["packagefile"]
        if existsDoubleKey(pack, "package", "name"):
            representation.name = pack["package"]["name"]
        end.append(representation)
    return end


def generateChroots(raw):
    end = []
    for pack in raw["chroots"]:
        representation = chrootmodel()
        if existsDoubleKey(pack, "chroot", "name"):
            representation.name = pack["chroot"]["name"]
        if existsDoubleKey(pack, "chroot", "mount"):
            representation.mountpoint = pack["chroot"]["mount"]
        end.append(representation)
    return end


def generateUsers(raw):
    end = []
    for pack in raw["users"]:
        representation = user()
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
