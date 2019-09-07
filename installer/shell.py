import subprocess


# A simple wrapper class that executes basic commands
class Command:
    def __init__(self, command="echo Hello World"):
        self.command = command
    # Executes a given command and returns the exit code
    def GetReturnCode(self):
        return subprocess.call(self.command, shell=True)  

    def GetSubProcess(self):
        return subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)

    def GetStdout(self):
        return self.GetSubProcess().stdout.read().replace(b"\n", b" ").decode('ascii')
