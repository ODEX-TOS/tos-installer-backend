#!/usr/bin/env python3
import argparse
import installer.parser.parse as parse
from installer.converter import convertYamlToCommands
import installer.parser.command as configs
import sys

parser = argparse.ArgumentParser(
    description='Generate system calls for installing operating systems')
parser.add_argument('-i', '--in', help='Input yaml file', default='')
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

def parseString(Input):
    parsed = parse.parseString(Input, config).execution
    command = convertYamlToCommands(parsed, config)
    return command

def parseToStdOut(file):
    commands = parser(file)
    for command in commands:
        print(command)


def parseToFile(fileIn, fileOut):
    commands = parser(fileIn)
    with open(fileOut, 'w') as f:
        for item in commands:
            f.write("%s\n" % item)

def parseFromStdInToFile(out):
    Input=""
    for line in sys.stdin.readlines():
            Input+=line+"\n"
    commands = parseString(Input)
    with open(out, 'w') as f:
        for item in commands:
            f.write("%s\n" % item)

def parsestd():
    Input=""
    for line in sys.stdin.readlines():
            Input+=line+"\n"
    commands = parseString(Input)
    for command in commands:
        print(command)

def getConfig():
    config = configs.parse(args["config"])
    return config


if __name__ == "__main__":
    config = getConfig()

    if args["out"] != '':
        if args["in"] != '':
            parseToFile(args["in"], args["out"])
        else:
            parseFromStdInToFile(args["out"])
    elif args["in"] != '':
        parseToStdOut(args["in"])
    else:
        parsestd()
