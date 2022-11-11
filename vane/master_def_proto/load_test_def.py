import yaml
from jinja2 import Template, Undefined
import sys

class NullUndefined(Undefined):
  def __getattr__(self, key):
    return ''
    

def main():
    print()

    try:
        with open('test_definition.yaml') as file:
            test_def = yaml.safe_load(file)
    except OSError:
        print('Couldnt not read test_definitions file')
        sys.exit()

    try:
        with open('master_def.yaml') as file:
            master_def = yaml.safe_load(file)
    except OSError:
        print('Could not read master test definitions file.')

    test_template = Template(str(test_def), undefined=NullUndefined)
    master_template = Template(str(master_def), undefined=NullUndefined)
    replace_data = yaml.safe_load(master_template.render())

    new = test_template.render(replace_data)
    yaml_new = yaml.safe_load(new)

    with open('replaced_file.yaml', 'w') as file:
        yaml.safe_dump(yaml_new, file, sort_keys=False)


if __name__ == "__main__":
    main()
