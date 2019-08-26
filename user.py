import shell
import crypt


class user:
    # groups is a list of groups
    def __init__(self, name, password, groups=["audio", "lp", "optical", "storage", "video", "wheel", "games", "power"], shell="/bin/bash", command="useradd -m -p {} -g users -G {} -s {} {} "):
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
        shell.command("mkhomedir_helper {}".format(self.name))

