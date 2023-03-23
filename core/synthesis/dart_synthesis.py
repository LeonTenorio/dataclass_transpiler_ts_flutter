import sys
import os

core_folder_path = os.path.abspath((os.path.dirname(sys.argv[0])))
sys.path.append(core_folder_path + '/utils/')
sys.path.append(core_folder_path + '/definition/')

from general_utils import reduce_array, replace_all, low_case_first_letter, map_and_join_array
from element_definition import ElementDefinition
from type_definition import TypeDefinition

def dart_synthesis_of_elements(map_of_elements, element_key, dart_hive_type_ids):
    element_definition = map_of_elements[element_key]

    element_text = _get_dart_text_of_element(element_definition, dart_hive_type_ids)

    return element_text

def _get_dart_text_of_element(element_definition, dart_hive_type_ids):
    element_name = element_definition.name
    class_type_definition = element_definition.class_type
    class_comment = element_definition.comment

    element_text = _create_comment(class_comment)

    additional_text = ''

    class_type_definition = element_definition.class_type
    use_hive = element_definition.use_hive

    main_class_name = None
    union_class_name = None
    intersection_class_name = None

    element_definition_enum = element_definition.enum

    if(element_definition_enum!=None):
        element_text = element_text + _get_text_of_enum_definition(element_definition_enum, use_hive, dart_hive_type_ids)
    else:
        class_type_definition_object_fields = class_type_definition.object_fields

        class_type_definition_unions = class_type_definition.unions
        class_type_definition_intersections = class_type_definition.intersections
        if(class_type_definition_object_fields!=None):
            main_class_name = element_name

            element_text = element_text + '@freezed\n' + \
                        'class ' + element_name + ' with _$' + element_name + ' {\n'
            
            element_text = element_text + _get_models_boxes_text(use_hive, element_name, None)

            element_text = element_text + '  const factory ' + element_name + '({\n'

            for field in class_type_definition_object_fields:
                field_text, field_additional_text = _get_text_of_type_field_definition(
                    field, 
                    element_name, 
                    use_hive,
                    dart_hive_type_ids
                )
                element_text = element_text + field_text  + ',\n'
                additional_text = additional_text + field_additional_text

            element_text = element_text + '  }) = _' + element_name + ';\n\n' + \
                        '  factory ' + element_name + '.fromJson(\n' + \
                        '    Map<String, dynamic> json,\n' + \
                        '  ) => \n' + \
                        '    _$' + element_name + 'FromJson(json);\n' + \
                        '}\n'

        if(class_type_definition_unions!=None):
            union_class_name = element_name

            if(main_class_name!=None):
                element_text = replace_all(element_text, main_class_name, main_class_name + 'MainUnionType')

            subclasses_names = []

            deserialization_text = '  late final Object _value;\n\n' + \
                                '  ' + union_class_name + '.fromJson(Map<String, dynamic> json){\n' + \
                                '    final deserializationFunctions = [\n'
            as_final_classes_text = ''
            serialization_text = '  Map<String, dynamic> toJson(){\n' + \
                                '    final List<Tuple2<bool Function(), Map<String, dynamic> Function()>> evaluateClasses = [\n'
            unions_to_create_object = class_type_definition_unions.copy()
            
            if(main_class_name!=None):
                unions_to_create_object.append(main_class_name + 'MainUnionType')
            
            for index, union in enumerate(unions_to_create_object):
                union_object_name, union_additional_text = _get_text_of_type_definition(
                    union, element_name + 'Union' + str(index), 
                    use_hive,
                    dart_hive_type_ids
                )
                additional_text = additional_text + union_additional_text

                subclasses_names.append(union_object_name)

                deserialization_text = deserialization_text + '      (json) => ' + union_object_name + '.fromJson(json),\n'

                is_union_object_function_name = 'is' + union_object_name
                as_union_object_function_name = 'as' + union_object_name

                as_final_classes_text = as_final_classes_text + '  bool ' + is_union_object_function_name + '() {\n' + \
                                        '    return _value is ' + union_object_name + ';\n' + \
                                        '  }\n\n' + \
                                        '  ' + union_object_name + ' ' + as_union_object_function_name + '(){\n' + \
                                        '    return _value as ' + union_object_name + ';\n' + \
                                        '  }\n\n'
                                        
                serialization_text = serialization_text + '      Tuple2(this.' + is_union_object_function_name + ', this.' + as_union_object_function_name + '),\n'

            constructor_text = '  ' + union_class_name + '.fromValue({\n' + map_and_join_array(
                                    subclasses_names,
                                    lambda x: '    ' + x + '? ' + low_case_first_letter(x) + ',\n',
                                    lambda array: ''.join(array)
                                ) + '  }){\n' + \
                                '    _value = (\n' + map_and_join_array(
                                    subclasses_names,
                                    lambda x: '      '+ low_case_first_letter(x),
                                    lambda array: '??\n'.join(array)
                                ) + '\n' + \
                                '    )!;\n' + \
                                '  }\n'
            models_box_text = _get_models_boxes_text(use_hive, union_class_name, subclasses_names, is_union=True)

            deserialization_text = deserialization_text + '    ];\n\n' + \
                                '    for(final deserializationFunction in deserializationFunctions){\n' + \
                                '      try{\n' + \
                                '        _value = deserializationFunction(json);\n' + \
                                '      } catch (_) {}\n' + \
                                '    }\n' + \
                                '  }\n'
            serialization_text = serialization_text + '    ];\n\n' + \
                                '    for(final evaluateClass in evaluateClasses){\n' + \
                                '      final isClass = evaluateClass.value1();\n' + \
                                '      if(isClass()){\n' + \
                                '        return evaluateClass.value2().toJson();\n' + \
                                '      }\n' + \
                                '    }\n' + \
                                '  }\n'

            element_text = element_text + 'class ' + union_class_name + '{\n' + \
                                    deserialization_text + '\n'+ \
                                    serialization_text + '\n' + \
                                    constructor_text + '\n' + \
                                    models_box_text + '\n' + \
                                    as_final_classes_text + \
                                    '}\n'

        if(class_type_definition_intersections!=None):
            intersection_class_name = element_name
            if(union_class_name!=None):
                element_text = replace_all(element_text, union_class_name, union_class_name + 'MainIntersectionType')

            elif(main_class_name!=None):
                element_text = replace_all(element_text, main_class_name, main_class_name + 'MainIntersectionType')

            deserialization_text = '  ' + intersection_class_name + '.fromJson(Map<String, dynamic> json){\n' + \
                                '    this._values = [];\n'
            as_final_classes_text = ''
            serialization_text = '  Map<String, dynamic> toJson(){\n' + \
                                '    return this._values.map((e) => (e as dynamic).toJson()).reduce((a, b) => a..addAll(b));\n' + \
                                '  }\n'
            
            intersections_to_create_object = class_type_definition_intersections.copy()
            
            if(union_class_name!=None):
                intersections_to_create_object.append(union_class_name + 'MainIntersectionType')
            elif(main_class_name!=None):
                intersections_to_create_object.append(main_class_name + 'MainIntersectionType')
            
            subclasses_names = []

            for index, intersection in enumerate(intersections_to_create_object):
                intersection_object_name, intersection_additional_text = _get_text_of_type_definition(
                    intersection, 
                    element_name + 'Intersection' + str(index), 
                    use_hive,
                    dart_hive_type_ids
                )
                additional_text = additional_text + intersection_additional_text

                subclasses_names.append(intersection_object_name)

                deserialization_text = deserialization_text + '    this._values.add(' + intersection_object_name + '.fromJson(json));\n'
                as_final_classes_text = as_final_classes_text + '  ' + intersection_object_name + ' as' + intersection_object_name + '(){\n'+ \
                                        '    return this._values[' + str(index) + '] as ' +intersection_object_name + ';\n'\
                                        '  }\n'
            deserialization_text = deserialization_text + '  }\n'

            constructor_text = '  ' + intersection_class_name + '.fromValues({\n' + map_and_join_array(
                                    subclasses_names,
                                    lambda x: '    required ' + x + ' ' + low_case_first_letter(x) + ',\n',
                                    lambda array: ''.join(array)
                                ) + '  }){\n' + \
                                '    _values = [\n' + map_and_join_array(
                                    subclasses_names,
                                    lambda x: '      '+ low_case_first_letter(x),
                                    lambda array: ',\n'.join(array)
                                ) + '\n' + \
                                '    ];\n' + \
                                '  }\n'

            element_text = element_text + 'class ' + intersection_class_name + ' {\n' + \
                        '  late final List<Object> _values;\n\n' + \
                        deserialization_text + '\n' + \
                        serialization_text + '\n' + \
                        constructor_text + '\n' + \
                        as_final_classes_text + \
                        '}\n'

    if(use_hive and element_definition_enum==None):
        hive_text = ''
        hive_element_name = ''
        
        if(intersection_class_name!=None):
            hive_element_name = main_class_name + 'MainIntersectionType'
        elif(union_class_name!=None):
            hive_element_name = main_class_name + 'MainUnionType'
        else:
            hive_element_name = main_class_name
        if(hive_element_name != None and len(hive_element_name)!=0):
            text_to_find = '  const factory ' + element_name + '({\n'
            element_text = replace_all(
                element_text, 
                text_to_find, 
                '  @HiveTypeId(typeId: ' + dart_hive_type_ids.get_hive_type_id(hive_element_name) + ')\n' + \
                text_to_find
            )   

    result_text = '\n' + element_text
    if(len(additional_text)>0):
        result_text = result_text + '\n' + additional_text

    return result_text

def _get_text_of_enum_definition(enum_definition, use_hive, dart_hive_type_ids):
    enum_text = _create_comment(enum_definition.comment)

    if(use_hive):
        enum_text = enum_text + '@HiveType(typeId: ' + dart_hive_type_ids.get_hive_type_id(enum_definition.name) + ')\n'

    enum_text = enum_text + 'enum ' + enum_definition.name + '{\n'

    for option_index, option in enumerate(enum_definition.enum_options):
        option_name = option.name
        option_value = option.value
        option_comment = option.comment

        option_text = _create_comment(option_comment, '  ') + '  '

        if(option_value!=None):
            option_text = option_text + '@JsonValue(' + str(option_value) + ')\n  '
        if(use_hive):
            hive_number_field = None
            if(option_value!=None):
                hive_number_field = option_value
            else:
                hive_number_field = option_index
            option_text = option_text + '@HiveField(' + str(hive_number_field) + ')\n  '
        option_text = option_text + option_name + ',\n'

        enum_text = enum_text + option_text
    
    enum_text = enum_text + '}\n'

    return enum_text

def _get_text_of_type_definition(type_definition, base_name, use_hive, dart_hive_type_ids):
    if(type(type_definition)==str):
        return type_definition, ''

    if(type_definition.simple_type!=None):
        return type_definition.simple_type, ''
    
    return _get_dart_text_of_element(
        _create_new_element_definition(
            base_name,
            type_definition,
            '',
            False,
            use_hive,
            False
        ),
        dart_hive_type_ids
    )


def _get_text_of_type_field_definition(type_field_definition, father_class_name, use_hive, dart_hive_type_ids):
    field_text = ''
    additional_text = ''

    type_definition = type_field_definition.type_definition
    enum_definition = type_field_definition.enum
    field_name = type_field_definition.name
    field_comment = type_field_definition.comment

    field_text = field_text + _create_comment(field_comment, line_indentation = '    ') + '    '

    if(type_field_definition.optional == False):
        field_text = field_text + 'required '
    if(enum_definition!=None):
        field_text = field_text + enum_definition.name + ' '

        additional_text = additional_text + _get_text_of_enum_definition(enum_definition, use_hive, dart_hive_type_ids)
    elif(type_definition.simple_type != None):
        field_text = field_text + _get_dart_simple_type(type_definition.simple_type) + ' '
    else:
        additional_field_type_name = field_name + 'AdditionalType' + father_class_name
        field_text = field_text + additional_field_type_name + ' '
        additional_element_name = additional_field_type_name

        additional_field_comment = 'additional type of field ' + field_name + ' from class ' + father_class_name
        if(field_comment!=None):
            additional_field_comment = additional_field_comment + '\n' + field_comment
        additional_text = _get_dart_text_of_element(
            _create_new_element_definition(
                additional_element_name,
                type_definition,
                additional_field_comment,
                False,
                use_hive,
                False
            ),
            dart_hive_type_ids
        )
    if(type_field_definition.nullable):
        field_text = field_text + '? '
    field_text = field_text + field_name

    return field_text, additional_text


def _create_new_element_definition(name, class_type, comment, exportable, use_hive, ts_validation):
    class_definition = ElementDefinition(name, [])
    class_definition.class_type = class_type
    class_definition.comment = comment
    class_definition.exportable  = exportable
    class_definition.use_hive = use_hive
    class_definition.ts_validation = ts_validation
    
    return class_definition

def _create_new_type_definition(simple_type, object_fields, unions, intersections):
    type_definition = TypeDefinition([])
    type_definition.simple_type = simple_type
    type_definition.object_fields = object_fields
    type_definition.unions = unions
    type_definition.intersections = intersections

    return type_definition


def _get_dart_simple_type(type):
    if(type == reserved_integer):
        return 'int'
    if(type == reserved_double):
        return 'double'
    elif(type == reserved_boolean):
        return 'bool'
    elif(type == reserved_date):
        return 'DateTime'
    elif(type == reserved_string):
        return 'String'
    return type

def _create_comment(comment, line_indentation = '', line_amount_of_letters = 80):
    if(comment==None):
        return ''
    lines = []
    actual_line = line_indentation + "/// "

    for word in comment.split(" "):
        if(len(actual_line) + len(word) < line_amount_of_letters):
            actual_line = actual_line + word + " "
        else:
            lines.append(actual_line)
            actual_line = line_indentation + "/// " +  word + " "
    lines.append(actual_line)

    if(len(lines)==0):
        return ''

    return '\n'.join(lines) + '\n'

def _is_primitive_type(a):
    if (a == None):
        return False
    return (
        a == reserved_boolean or
        a == reserved_integer or
        a == reserved_double or 
        a == reserved_date or 
        a == reserved_string
    )

def _union_of_primitive_type(a, b):
    if(_is_primitive_type(a)==False or _is_primitive_type(b)==False):
        return None
    if(
        (a == reserved_boolean and b == reserved_integer) or
        (a == reserved_integer and b == reserved_boolean)
    ):
        return reserved_integer
    if(
        (a == reserved_double and b == reserved_integer) or
        (a == reserved_integer and b == reserved_double) or
        (a == reserved_double and b == reserved_boolean) or
        (a == reserved_boolean and b == reserved_double)
    ):
        return reserved_double
    if(
        (a == reserved_string and b == reserved_date) or 
        (a == reserved_date and b == reserved_string)
    ):
        return reserved_string
    return None
    
def _get_models_boxes_text(use_hive, class_name, subclasses_names, is_union = False, is_intersection = False):
    if(use_hive==False):
        return ''
    if(subclasses_names==None):
        return '  static ModelsBox<' + class_name + '> getBox() {\n' + \
               '    final box = Hive.box<' + class_name + '>(' + 'HiveTypeIds.' + class_name + '.toString());\n' + \
               '    return ModelsBox<' + class_name + '>(\n' + \
               '      get: (key) => key.startsWith("_")? null: box.get(key),\n' + \
               '      put: (key, value) => box.put(key, value),\n' + \
               '      delete: (key) async {\n' + \
               '        if(key.startsWith("_")) return;\n' + \
               '        await box.delete(key);\n' + \
               '      },\n' + \
               '      clear: () async {\n' + \
               '        await box.deleteAll(box.keys.map((key) => key as String).where((key) => !key.startsWith("_")));\n' + \
               '      },\n' + \
               '      values: () => box.keys.map((key) => key as String).where((key) => !key.startsWith("_")).map(box.get),\n' + \
               '      keys: () => box.keys.map((key) => key as String).where((key) => !key.startsWith("_")),\n' + \
               '    );\n' + \
               '  }\n\n'
    if(is_union):
        union_class_name = class_name

        models_box_boxes_prefix_text = []
        models_box_boxes_variables_text = []
        models_box_boxes_getters_text = []
        models_box_boxes_put_text = []
        models_box_boxes_delete_text = []
        models_box_boxes_clear_text = []
        models_box_boxes_values_text = []
        models_box_boxes_keys_text = []

        for subclass_name in subclasses_names:
            models_box_variable_prefix = low_case_first_letter(subclass_name) + 'KeyPrefix'
            models_box_variable_name = low_case_first_letter(subclass_name) + 'Box'
            models_box_boxes_prefix_text.append(
                'final ' + models_box_variable_prefix + ' = ' + \
                ' "_union-'+union_class_name+'-'+subclass_name+'"'
            )
            models_box_boxes_variables_text.append(
                'final ' + models_box_variable_name + ' = ' + \
                'Hive.box<' + subclass_name + '>(HiveTypeIds.' + \
                subclass_name + '.toString()'
                ')'
            )
            models_box_boxes_getters_text.append(models_box_variable_name + '.get(' + models_box_variable_prefix + ' + key)')
            models_box_boxes_put_text.append('if (value is ' + subclass_name+ ') {')
            models_box_boxes_put_text.append('  await ' + models_box_variable_name + '.put(' + models_box_variable_prefix + ' + key, value);')
            models_box_boxes_put_text.append('}')
            models_box_boxes_delete_text.append(models_box_variable_name + '.delete(' + models_box_variable_prefix + 'key)')
            models_box_boxes_clear_text.append(
                models_box_variable_name + '.deleteAll(' + \
                models_box_variable_name + '.keys.map((key) => key as String).where((key) => ' + \
                'key.startsWith(' + models_box_variable_prefix + ')' + \
                ')' + \
                ')'
            )
            models_box_boxes_values_text.append(
                'listOfValues.addAll(' + \
                models_box_variable_name + '.keys.map((key) => key as String)' + \
                '.where((key) => key.startsWith('+models_box_variable_prefix+'))' + \
                '.map((key) => '+ \
                union_class_name + '.fromValue({' + \
                low_case_first_letter(subclass_name) + ': ' + \
                models_box_variable_name + '.get(key)!'
                '})' + \
                ')'
                '.map((key) => '+models_box_variable_name+'.get(key)!)'
            )
            models_box_boxes_keys_text.append(
                'keys.addAll(' + \
                models_box_variable_name + '.keys.map((key) => key as String)' + \
                '.where((key) => key.startsWith('+models_box_variable_prefix+'))' + \
                ')'
            )

        models_box_text = '  static ModelsBox<' + union_class_name + '> getBox() {\n' + \
                            map_and_join_array(
                                models_box_boxes_prefix_text,
                                lambda x: '    ' + x + ';',
                                lambda array: '\n'.join(array)
                            ) + '\n' + \
                            map_and_join_array(
                                models_box_boxes_variables_text,
                                lambda x: '    ' + x + ';',
                                lambda array: '\n'.join(array)
                            ) + '\n' + \
                            '    return ModelsBox<' + union_class_name + '>(\n' \
                            '      get: (key) { \n' + \
                            '        return (\n' + \
                            map_and_join_array(
                                models_box_boxes_getters_text,
                                lambda x: '          ' + x,
                                lambda array: ' ??\n'.join(array)
                            ) + '\n'+\
                            '        );\n'+ \
                            '      },\n' + \
                            '      put: (key, value) async {\n' + \
                            map_and_join_array(
                                models_box_boxes_put_text,
                                lambda x: '        ' + x,
                                lambda array: '\n'.join(array)
                            ) + '\n' + \
                            '      },\n' + \
                            '      delete: (key) async {\n' + \
                            '        await Future.wait([\n' + \
                            map_and_join_array(
                                models_box_boxes_delete_text,
                                lambda x: '          ' + x + ',',
                                lambda array: '\n'.join(array)
                            ) + '\n' +\
                            '        ]);\n' + \
                            '      },\n' + \
                            '      clear: () async {\n' + \
                            '        await Future.wait([\n' + \
                            map_and_join_array(
                                models_box_boxes_clear_text,
                                lambda x: '          ' + x + ',',
                                lambda array: '\n'.join(array)
                            ) + '\n' +\
                            '        ]);\n' + \
                            '      },\n' + \
                            '      values: () {\n' + \
                            '        List<' + union_class_name + '> listOfValues = [];\n' + \
                            map_and_join_array(
                                models_box_boxes_values_text,
                                lambda x: '        ' + x + ';',
                                lambda array: '\n'.join(array)
                            ) + '\n' + \
                            '        return Iterable.castFrom<' +union_class_name+ ', ' + union_class_name + '>(listOfValues);\n' + \
                            '      },\n' + \
                            '      keys: () {\n' + \
                            '        List<String> keys = [];\n' + \
                            map_and_join_array(
                                models_box_boxes_keys_text,
                                lambda x: '        ' + x + ';',
                                lambda array: '\n'.join(array)
                            ) + '\n' + \
                            '        return Iterable.castFrom<String, String>(keys);\n' + \
                            '      },\n' + \
                            '    );\n' + \
                            '  }\n'
        return models_box_text
    

reserved_integer = 'integer'
reserved_double = 'double'
reserved_boolean = 'boolean'
reserved_date = 'date'
reserved_string = 'string'