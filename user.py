import shell
import crypt
import config


class user:
    # groups is a list of groups
    def __init__(self, name, password, groups=config.GROUPS, shell=config.DEFAULT_SHELL, command=config.USERADD):
        self.name = name
        self.password = password
        self.groups = groups
        self.shell = shell
        self.command = command

    def getEncryptedPassword(self):
        return crypt.crypt(self.password, "password")


    
    def createUser(self):
        groups = ""
        for group in self.groups:
            groups += group + ","

        command =self.command.format(self.getEncryptedPassword(), groups[:-1], self.shell, self.name) 
        print(command)
        shell.Command(command).GetStdout()

    def createHome(self):
        shell.command(config.USER_HOME_BUILDER.format(self.name))

