# TODO: add a config section


class file:
    """
    A class based representation of the config file
    """

    def __init__(self):
        self.model = None
        self.execution = None

    def __str__(self):
        return "YAML : \n {} \n\n\n {}".format(self.model, self.execution)
