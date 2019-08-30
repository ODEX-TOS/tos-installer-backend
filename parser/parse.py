import yaml
import parser.yamlfile as yamlfile
import parser.model as model
import parser.execution as execution


def generate(raw):
    """
    Convert raw yaml convertion to a class based representation
    """
    representation = yamlfile.file()
    representation.model = model.generateModel(raw["models"])
    representation.execution = execution.generateExecution(raw["execution"])
    return representation


def modelLinker(file):
    """
    convert a raw yamlfile.file object to a linked model to executor linker
    It will link generated models to executors. So that each executor knows with which model to work with
    """
    for executor in file.execution.steps:
        executor.setModel(file.model)
        if type(executor) == type(execution.chroot()):
            for step in executor.steps:
                step.setModel(file.model)
    return file


def parse(filename):
    with open(filename, 'r') as stream:
        try:
            content = yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
    return modelLinker(generate(content))


if __name__ == "__main__":
    with open("example.yaml", 'r') as stream:
        try:
            content = yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
    print(modelLinker(generate(content)))
