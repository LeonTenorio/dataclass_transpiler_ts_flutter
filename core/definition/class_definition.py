import sys
import os

core_folder_path = os.path.abspath((os.path.dirname(sys.argv[0])))
sys.path.append(core_folder_path + '/definition/')
sys.path.append(core_folder_path + '/utils/')

from type_definition import TypeDefinition
from yaml_utils import get_boolean_of_yaml

class ClassDefinition:
    def __init__(self, name, yaml_content):
        self.name = name
        self.class_type, self.exportable, self.use_hive, self.ts_validation = self._get_class_definition(yaml_content)
    def _get_class_definition(self, yaml_content):
        class_type = None
        use_hive = False
        ts_validation = False
        exportable = False

        effective_yaml_content = yaml_content
        if(type(effective_yaml_content)!=list):
            effective_yaml_content = [effective_yaml_content]
        for item in effective_yaml_content:
            key = list(item.keys())[0]
            content = item[key]
            if(key == reserved_type):
                class_type = TypeDefinition(content)
            elif(key == reserved_exportable):
                exportable = get_boolean_of_yaml(content)
            elif(key == reserved_use_hive):
                use_hive = get_boolean_of_yaml(content)
            elif(key == reserved_ts_validation):
                ts_validation = get_boolean_of_yaml(content)
        
        return class_type, exportable, use_hive, ts_validation
    def __str__(self):
        return 'ClassDefinition(name: ' + self.name + \
               ', type: ' + str(self.class_type) + \
               ', exportable: ' + str(self.exportable) + \
               ', useHive: ' + str(self.use_hive) + \
               ', tsValidation: ' + str(self.ts_validation) + ')'

reserved_type = 'type'
reserved_exportable = 'exportable'
reserved_use_hive = 'useHive'
reserved_ts_validation = 'tsValidation'