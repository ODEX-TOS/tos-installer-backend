#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2019 Meyers Tom
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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

