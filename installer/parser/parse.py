
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
import yaml
import installer.parser.yamlfile as yamlfile
import installer.parser.model as model
import installer.parser.execution as execution


def generate(raw, config):
    """
    Convert raw yaml convertion to a class based representation
    """
    representation = yamlfile.file()
    representation.model = model.generateModel(raw["models"], config)
    representation.execution = execution.generateExecution(
        raw["execution"], config)
    return representation


def modelLinker(file):
    """
    convert a raw yamlfile.file object to a linked model to executor linker
    It will link generated models to executors. So that each executor knows with which model to work with
    """
    for executor in file.execution.steps:
        executor.setModel(file.model)
        if type(executor) == type(execution.chroot({"MOUNTPOINT": ""})):
            for step in executor.steps:
                step.setModel(file.model)
    return file


def parse(filename, config):
    with open(filename, 'r') as stream:
        try:
            content = yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
    return modelLinker(generate(content, config))

def parseString(string, config):
        try:
            content = yaml.load(string, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
        return modelLinker(generate(content, config))

if __name__ == "__main__":
    with open("example.yaml", 'r') as stream:
        try:
            content = yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
    print(modelLinker(generate(content)))
