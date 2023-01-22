import sys
import os

core_folder_path = os.path.abspath((os.path.dirname(sys.argv[0])))
sys.path.append(core_folder_path + '/definition/')
sys.path.append(core_folder_path + '/utils/')

from class_definition import ClassDefinition
from general_utils import map_and_join_array

class YamlDefinition:
    def __init__(self, file_name, yaml_content):
        self.file_name = file_name
        self.classes, self.imports = self._get_class_definition(yaml_content)
    def _get_class_definition(self, yaml_content):
        classes = []
        imports = []
        for item in yaml_content:
            key = list(item.keys())[0]
            content = item[key]
            if(key == reserved_imports):
                imports = content
                if(type(imports)!=list):
                    imports = [imports]
            else:
                classes.append(ClassDefinition(key, content))

        return classes, imports
    def __str__(self):
        return '\n-----------------------------------------------------------\n' + \
               'File name: ' + self.file_name + '\n' + \
               'Imports: ' + map_and_join_array(self.imports, lambda x: str(x), lambda x: ', '.join(x)) + \
               '\nClasses: \n' + map_and_join_array(self.classes, lambda x: str(x), lambda x: '\n'.join(x)) + \
               '\n-----------------------------------------------------------\n'

reserved_imports = 'imports'