import os
from fnmatch import fnmatch
import yaml

def get_boolean_of_yaml(value):
    if(type(value)==bool):
        return value
    if(value.casefold()=='false'):
        return False
    elif(value.casefold()=='true'):
        return True
    else:
        return None

def read_yaml_content(file_name):
    with open(file_name, 'r') as f:
        try:
            file_content = yaml.safe_load(f)
            return file_content
        except yaml.YAMLError as exc:
            print(exc)
            print('Something wrong with the file: '+file_path)
            exit(-1)

def get_yaml_file_list():
    pattern = '*.yaml'

    file_list = []
    for path, subdirs, files in os.walk('./'):
        for name in files:
            if fnmatch(name, pattern):
                file_path = os.path.join(path, name)
                file_list.append(file_path)
    
    return file_list