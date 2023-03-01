import sys
import os

core_folder_path = os.path.abspath((os.path.dirname(sys.argv[0])))
sys.path.append(core_folder_path + '/utils/')

from general_utils import map_and_join_array, nullable_text

class EnumDefinition:
    def __init__(self, name, yaml_content):
        self.name = name
        self.enum_options, self.comment = self._get_enum_definition(yaml_content)
    def _get_enum_definition(self, yaml_content):
        comment = None
        enum_options = []
        
        for key in yaml_content.keys():
            item = yaml_content[key]
            if(key == reserved_comment):
                comment = item
            elif(key == reserved_values):
                values_list = item
                if(type(values_list)!=list):
                    values_list = [values_list]
                for item in values_list:
                    enum_option_name = None
                    enum_option_value = None
                    enum_option_comment = None
                    if(type(item)==str):
                        enum_option_name = item
                    elif(type(item)==dict):
                        enum_option_name = list(item.keys())[0]
                        enum_option_definition = item[enum_option_name]

                        for key in enum_option_definition.keys():
                            enum_option_definition_item = enum_option_definition[key]
                            if(key == reserved_enum_option_value):
                                enum_option_value = enum_option_definition_item
                            elif(key == reserved_comment):
                                enum_option_comment = enum_option_definition_item

                    enum_options.append(EnumOptionDefinition(enum_option_name, enum_option_value, enum_option_comment))

        return enum_options, comment

    def __str__(self):
        return 'EnumDefinition( ' + map_and_join_array(self.enum_options, lambda x: str(x), lambda array: ', '.join(array)) + ')'

class EnumOptionDefinition:
    def __init__(self, name, value, comment):
        self.name = name
        self.value = value
        self.comment = comment
    def __str__(self):
        return 'EnumOptionDefinition(name: ' + self.name + \
               ', comment: ' + nullable_text(self.comment) + \
               ', value: ' + nullable_text(self.value) + \
               ')'
    
reserved_enum_option_value = 'value'
reserved_comment = 'comment'
reserved_values = 'values'