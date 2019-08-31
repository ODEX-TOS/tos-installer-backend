import argparse
import config
import parser.parse as parse
from converter import convertYamlToCommands


parser = argparse.ArgumentParser(
    description='Generate system calls for installing operating systems')
parser.add_argument('-i', '--in', help='Input yaml file', default='')
parser.add_argument(
    '-o', '--out', help='File to output generated script', default='')

args = vars(parser.parse_args())


def parser(file):
    parsed = parse.parse(file).execution
    commands = convertYamlToCommands(parsed)
    return commands


def parseToStdOut(file):
    commands = parser(file)
    for command in commands:
        print(command)


def parseToFile(fileIn, fileOut):
    commands = parser(fileIn)
    with open(fileOut, 'w') as f:
        for item in commands:
            f.write("%s\n" % item)


if __name__ == "__main__":
    if args["in"] != '':
        if args["out"] != '':
            parseToFile(args["in"], args["out"])
        else:
            parseToStdOut(args["in"])
    else:
        if args["out"] != '':
            parseToFile("config.yaml", args["out"])
        else:
            parseToStdOut("config.yaml")
