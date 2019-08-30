
class execution:
    """
    A class defined in the yaml file as executions
    It holds a list of execution steps
    """

    def __init__(self):
        self.steps = [None]

    def __str__(self):
        string = ""
        for step in self.steps:
            string += "\n\t\t" + str(step)
        return "Execution:\n{}".format(string)


class partitiontable:
    """
    The execution step called partitiontable
    It builds the partitiontable
    """

    def __init__(self):
        self.model = None

    def __str__(self):
        return "PartitionTabel -- model {}".format(self.model)


class format:
    """
    The execution step called format
    It formats a partition/drive
    """

    def __init__(self):
        self.model = None

    def __str__(self):
        return "Format -- model {}".format(self.model)


class mount:
    """
    The execution step called mount
    It mount a partition or disk to a mountpoint
    """

    def __init__(self):
        self.model = None

    def __str__(self):
        return "mount -- model {}".format(self.model)


class bootstrap:
    """
    The execution step called bootstrap
    It bootstraps packages to a mountpoint
    """

    def __init__(self):
        self.model = None

    def __str__(self):
        return "bootstrap -- model {}".format(self.model)


class fstab:
    """
    The execution step called fstab
    It builds the fstab file based on mounted partitions
    """

    def __init__(self):
        self.model = None

    def __str__(self):
        return "bootstrap -- model {}".format(self.model)


class chroot:
    """
    The execution step called chroot
    It changes the root mountpoint and executes build steps there
    """

    def __init__(self):
        self.user = None
        self.steps = [None]

    def __str__(self):
        steps = ""
        for step in self.steps:
            steps += "\t\t\t\t{}\n".format(step)
        return "chroot -- user: {} -- steps: \n{}".format(self.user, steps)


class systemsetup:
    """
    The execution step called systemsetup
    It builds the basic system information
    """

    def __init__(self):
        self.model = None

    def __str__(self):
        return "systemsetup -- model {}".format(self.model)


class createUser:
    """
    The execution step called createUser
    It creates a basic unix user
    """

    def __init__(self):
        self.model = None

    def __str__(self):
        return "user -- model {}".format(self.model)


class bootloaderstep:
    """
    The execution step called bootloader
    It generates the bootloader configurations
    """

    def __init__(self):
        self.model = None

    def __str__(self):
        return "bootloader -- model {}".format(self.model)


class packages:
    """
    The execution step called packages
    It installs packages on your system
    """

    def __init__(self):
        self.model = None

    def __str__(self):
        return "packages -- model {}".format(self.model)


class scriptstep:
    """
    The execution step called script
    It executes a script
    """

    def __init__(self):
        self.model = None

    def __str__(self):
        return "script -- model {}".format(self.model)


def generateExecution(raw):
    """
    generate a execution from a raw yaml model
    """
    steps = []
    for step in raw:
        steps.append(getStep(step))
    executor = execution()
    executor.steps = steps
    return executor


def getStep(raw):
    """
    Detect the type of the build step and generate a model from it
    """
    print(raw)
    if exists(raw, "partitiontable"):
        ptable = partitiontable()
        ptable.model = raw["partitiontable"]
        return ptable
    if exists(raw, "format"):
        form = format()
        form.model = raw["format"]
        return form
    if exists(raw, "mount"):
        mounter = mount()
        mounter.model = raw["mount"]
        return mounter
    if exists(raw, "bootstrap"):
        boot = bootstrap()
        boot.model = raw["bootstrap"]
        return boot
    if exists(raw, "fstab"):
        stab = fstab()
        stab.model = raw["fstab"]
        return stab
    if exists(raw, "systemsetup"):
        setup = systemsetup()
        setup.model = raw["systemsetup"]
        return setup
    if exists(raw, "createuser"):
        setup = createUser()
        setup.model = raw["createuser"]
        return setup
    if exists(raw, "bootloader"):
        loader = bootloaderstep()
        loader.model = raw["bootloader"]
        return loader
    if exists(raw, "chroot"):
        root = chroot()
        root.user = raw["chroot"]["user"]
        root.steps = []
        for item in raw["chroot"]["steps"]:
            root.steps.append(getStep(item))
        return root
    return raw


def exists(dict, key):
    return key in dict.keys()


def existsDoubleKey(dict, key1, key2):
    return key1 in dict.keys() and key2 in dict[key1]
