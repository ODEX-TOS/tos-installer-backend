import argparse
import parser.parse as parse
from converter import convertYamlToCommands
import parser.command as configs


parser = argparse.ArgumentParser(
    description='Generate system calls for installing operating systems')
parser.add_argument('-i', '--in', help='Input yaml file', default='data.yaml')
parser.add_argument(
    '-o', '--out', help='File to output generated script', default='')
parser.add_argument(
    '-c', '--config', help='Set a custom config script to load', default='config.yaml')

args = vars(parser.parse_args())
config = None


def parser(file):
    parsed = parse.parse(file, config).execution
    commands = convertYamlToCommands(parsed, config)
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


def getConfig():
    config = configs.parse(args["config"])
    return config


if __name__ == "__main__":
    config = getConfig()

    if args["out"] != '':
        parseToFile(args["in"], args["out"])
    else:
        parseToStdOut(args["in"])
