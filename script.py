import shell


def executeExternalScript(filename):
    with open(filename, 'r') as file:
            data = file.read()
    return shell.Command(data).GetStdout()
