
class execution:
    """
    A class defined in the yaml file as executions
    It holds a list of execution steps
    """

    def __init__(self):
        self.steps = [None]


class partitiontable:
    """
    The execution step called partitiontable
    It builds the partitiontable
    """

    def __init__(self):
        self.model = None


class format:
    """
    The execution step called format
    It formats a partition/drive
    """

    def __init__(self):
        self.model = None


class mount:
    """
    The execution step called mount
    It mount a partition or disk to a mountpoint
    """

    def __init__(self):
        self.model = None


class bootstrap:
    """
    The execution step called bootstrap
    It bootstraps packages to a mountpoint
    """

    def __init__(self):
        self.model = None


class fstab:
    """
    The execution step called fstab
    It builds the fstab file based on mounted partitions
    """

    def __init__(self):
        self.model = None


class chroot:
    """
    The execution step called chroot
    It changes the root mountpoint and executes build steps there
    """

    def __init__(self):
        self.user = None
        self.steps = [None]


class systemsetup:
    """
    The execution step called systemsetup
    It builds the basic system information
    """

    def __init__(self):
        self.model = None


class createUser:
    """
    The execution step called createUser
    It creates a basic unix user
    """

    def __init__(self):
        self.model = None


class bootloaderstep:
    """
    The execution step called bootloader
    It generates the bootloader configurations
    """

    def __init__(self):
        self.model = None


class packages:
    """
    The execution step called packages
    It installs packages on your system
    """

    def __init__(self):
        self.model = None


class scriptstep:
    """
    The execution step called script
    It executes a script
    """

    def __init__(self):
        self.model = None


def generateExecution(raw):
    """
    generate a execution from a raw yaml model
    """
    return raw
