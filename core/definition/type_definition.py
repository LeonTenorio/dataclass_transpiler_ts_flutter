import sys
import os

core_folder_path = os.path.abspath((os.path.dirname(sys.argv[0])))
sys.path.append(core_folder_path + '/utils/')

from yaml_utils import get_boolean_of_yaml
from general_utils import map_array, map_and_join_array, nullable_text, nullable_element_function

class TypeDefinition:
    def __init__(self, yaml_content):
        self.simple_type, self.object_fields, self.unions, self.intersections = self._get_yaml_content(yaml_content)

    def _get_yaml_content(self, yaml_content):
        simple_type = None
        object_fields = None
        object_unions = None
        object_intersections = None

        effective_yaml_content = yaml_content
        if(type(effective_yaml_content)!=list):
            effective_yaml_content = [effective_yaml_content]
        
        for item in effective_yaml_content:
            if(type(item)==dict):
                for key in item.keys():
                    content = item[key]
                    if(type(content)!=list):
                        content = [content]
                    if(key == reserved_union):
                        object_unions = map_array(content, lambda x: TypeDefinition(x))
                    elif(key == reserved_intersection):
                        object_intersections = map_array(content, lambda x: TypeDefinition(x))
                    else:
                        if(object_fields == None):
                            object_fields = []
                        object_fields.append(TypeFieldDefinition(key, content))
            else:
                simple_type = item
        
        return simple_type, object_fields, object_unions, object_intersections
    def __str__(self):
        return 'TypeDefinition(simple type: ' + nullable_text(self.simple_type) + \
               ', fields: ' + nullable_element_function(
                    self.object_fields, 
                    lambda: '-', 
                    lambda object_fields: map_and_join_array(
                        object_fields, 
                        lambda field: str(field),
                        lambda fields: ', '.join(fields)
                    )
                ) + \
                ', unions: ' + nullable_element_function(
                    self.unions,
                    lambda: '-', 
                    lambda object_unions: map_and_join_array(
                        object_unions,
                        lambda union: str(union),
                        lambda unions: ', '.join(unions)
                    )
                ) + \
                ', intersections: ' + nullable_element_function(
                    self.intersections,
                    lambda: '-', 
                    lambda object_intersections: map_and_join_array(
                        object_intersections,
                        lambda intersection: str(intersection),
                        lambda intersections: ', '.join(intersections)
                    )
                )
        
class TypeFieldDefinition:
    def __init__(self, name, yaml_content):
        self.name = name
        self.type_definion, self.nullable, self.optional = self._get_type_field_definition(yaml_content)
    def _get_type_field_definition(self, yaml_content):
        nullable = False
        optional = False
        type_definition = None

        for item in yaml_content:
            for key in item.keys():
                content = item[key]
                if(key == reserved_type):
                    type_definition = TypeDefinition(content)
                elif(key == reserved_nullable):
                    nullable = get_boolean_of_yaml(content)
                elif(key == reserved_optional):
                    optional = get_boolean_of_yaml(content)
        
        return type_definition, nullable, optional

    def __str__(self):
        return 'TypeFieldDefinition(name:' + self.name + \
               ', nullable: ' + str(self.nullable) + \
               ', optional: ' + str(self.optional) + ')'
               
reserved_integer = 'integer'
reserved_double = 'double'
reserved_boolean = 'boolean'
reserved_date = 'date'
reserved_string = 'string'

reserved_type = 'type'
reserved_nullable = 'nullable'
reserved_optional = 'optional'

reserved_union = 'union'
reserved_intersection = 'intersection'