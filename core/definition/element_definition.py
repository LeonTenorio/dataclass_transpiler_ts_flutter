import sys
import os

core_folder_path = os.path.abspath((os.path.dirname(sys.argv[0])))
sys.path.append(core_folder_path + '/definition/')
sys.path.append(core_folder_path + '/utils/')

from type_definition import TypeDefinition
from enum_definition import EnumDefinition
from yaml_utils import get_boolean_of_yaml
from general_utils import nullable_text

class ElementDefinition:
    def __init__(self, name, yaml_content):
        self.name = name
        self.class_type, self.enum, self.comment, self.exportable, self.use_hive, self.ts_validation = self._get_class_definition(yaml_content)
    def _get_class_definition(self, yaml_content):
        class_type = None
        use_hive = False
        ts_validation = False
        exportable = False
        comment = None
        enum = None

        effective_yaml_content = yaml_content
        if(type(effective_yaml_content)!=list):
            effective_yaml_content = [effective_yaml_content]
        for item in effective_yaml_content:
            for key in item.keys():
                content = item[key]
                if(key == reserved_type):
                    class_type = TypeDefinition(content)
                elif(key == reserved_exportable):
                    exportable = get_boolean_of_yaml(content)
                elif(key == reserved_use_hive):
                    use_hive = get_boolean_of_yaml(content)
                elif(key == reserved_ts_validation):
                    ts_validation = get_boolean_of_yaml(content)
                elif(key == reserved_comment):
                    comment = content
                elif(key == reserved_enum):
                    enum = EnumDefinition(self.name, content)
        
        return class_type, enum, comment, exportable, use_hive, ts_validation
    def __str__(self):
        return 'ElementDefinition(name: ' + self.name + \
               ', comment: ' + nullable_text(self.comment) + \
               ', type: ' + nullable_text(self.class_type) + \
               ', enum: ' + nullable_text(self.enum) + \
               ', exportable: ' + str(self.exportable) + \
               ', useHive: ' + str(self.use_hive) + \
               ', tsValidation: ' + str(self.ts_validation) + ')'

reserved_type = 'type'
reserved_exportable = 'exportable'
reserved_use_hive = 'useHive'
reserved_ts_validation = 'tsValidation'
reserved_comment = 'comment'
reserved_enum = 'enum'