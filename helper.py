# helper functions for manipulating filesystems
import shell

# TODO: implement
def appendToFile(string, filename):
    return

# TODO: implement
def changeLineInFile(regex, newLine, filename):
    return

def removeFiles(files):
    for filename in files:
        shell.Command("rm -rf {}".format(filename)).GetReturnCode()

# TODO: implement
def createFileWithContent(filename, content):
    return
