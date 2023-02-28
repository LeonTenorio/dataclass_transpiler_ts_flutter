import sys
import os

core_folder_path = os.path.abspath((os.path.dirname(sys.argv[0])))
sys.path.append(core_folder_path + '/definition/')
sys.path.append(core_folder_path + '/utils/')

from element_definition import ElementDefinition
from general_utils import map_and_join_array

class YamlDefinition:
    def __init__(self, file_name, yaml_content):
        self.file_name = file_name
        self.elements, self.imports = self._get_elements_definition(yaml_content)
    def _get_elements_definition(self, yaml_content):
        elements = []
        imports = []
        for item in yaml_content:
            key = list(item.keys())[0]
            content = item[key]
            if(key == reserved_imports):
                imports = content
                if(type(imports)!=list):
                    imports = [imports]
            else:
                elements.append(ElementDefinition(key, content))

        return elements, imports
    def __str__(self):
        return '\n-----------------------------------------------------------\n' + \
               'File name: ' + self.file_name + '\n' + \
               'Imports: ' + map_and_join_array(self.imports, lambda x: str(x), lambda x: ', '.join(x)) + \
               '\Elements: \n' + map_and_join_array(self.classes, lambda x: str(x), lambda x: '\n'.join(x)) + \
               '\n-----------------------------------------------------------\n'

reserved_imports = 'imports'