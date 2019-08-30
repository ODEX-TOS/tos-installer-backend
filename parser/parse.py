import yaml
import yamlfile
import model
import execution


with open("example.yaml", 'r') as stream:
    try:
        content = yaml.load(stream, Loader=yaml.Loader)
    except yaml.YAMLError as exc:
        print(exc)


def generate(raw):
    """
    Convert raw yaml convertion to a class based representation
    """
    representation = yamlfile.file()
    representation.model = model.generateModel(raw["models"])
    representation.execution = execution.generateExecution(raw["execution"])
    return representation


if __name__ == "__main__":
    # print(content)
    print(generate(content).model)
