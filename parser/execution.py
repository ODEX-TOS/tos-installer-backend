
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
        self.reference = None

    def __str__(self):
        return "PartitionTabel -- reference: {} -- model {}".format(self.reference, self.model)


class format:
    """
    The execution step called format
    It formats a partition/drive
    """

    def __init__(self):
        self.model = None
        self.reference = None

    def __str__(self):
        return "Format -- reference: {} -- model {}".format(self.reference, self.model)


class mount:
    """
    The execution step called mount
    It mount a partition or disk to a mountpoint
    """

    def __init__(self):
        self.model = None
        self.reference = None

    def __str__(self):
        return "mount -- reference: {} -- model {}".format(self.reference, self.model)


class bootstrap:
    """
    The execution step called bootstrap
    It bootstraps packages to a mountpoint
    """

    def __init__(self):
        self.model = None
        self.reference = None

    def __str__(self):
        return "bootstrap -- reference: {} -- model {}".format(self.reference, self.model)


class fstab:
    """
    The execution step called fstab
    It builds the fstab file based on mounted partitions
    """

    def __init__(self):
        self.model = None
        self.reference = None

    def __str__(self):
        return "bootstrap -- reference: {} -- model {}".format(self.reference, self.model)


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
        self.reference = None

    def __str__(self):
        return "systemsetup -- reference: {} -- model {}".format(self.reference, self.model)


class createUser:
    """
    The execution step called createUser
    It creates a basic unix user
    """

    def __init__(self):
        self.model = None
        self.reference = None

    def __str__(self):
        return "user -- reference: {} -- model {}".format(self.reference, self.model)


class bootloaderstep:
    """
    The execution step called bootloader
    It generates the bootloader configurations
    """

    def __init__(self):
        self.model = None
        self.reference = None

    def __str__(self):
        return "bootloader -- reference: {} -- model {}".format(self.reference, self.model)


class packages:
    """
    The execution step called packages
    It installs packages on your system
    """

    def __init__(self):
        self.model = None
        self.reference = None

    def __str__(self):
        return "packages -- reference: {} -- model {}".format(self.reference, self.model)


class scriptstep:
    """
    The execution step called script
    It executes a script
    """

    def __init__(self):
        self.model = None
        self.reference = None

    def __str__(self):
        return "script -- reference: {} -- model {}".format(self.reference, self.model)


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
        ptable.reference = raw["partitiontable"]
        return ptable
    if exists(raw, "format"):
        form = format()
        form.reference = raw["format"]
        return form
    if exists(raw, "mount"):
        mounter = mount()
        mounter.reference = raw["mount"]
        return mounter
    if exists(raw, "bootstrap"):
        boot = bootstrap()
        boot.reference = raw["bootstrap"]
        return boot
    if exists(raw, "fstab"):
        stab = fstab()
        stab.reference = raw["fstab"]
        return stab
    if exists(raw, "systemsetup"):
        setup = systemsetup()
        setup.reference = raw["systemsetup"]
        return setup
    if exists(raw, "createuser"):
        setup = createUser()
        setup.reference = raw["createuser"]
        return setup
    if exists(raw, "bootloader"):
        loader = bootloaderstep()
        loader.reference = raw["bootloader"]
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
