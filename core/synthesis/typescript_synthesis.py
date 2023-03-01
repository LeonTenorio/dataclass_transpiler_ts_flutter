def ts_synthesis_of_elements(map_of_elements, element_key):
    element_definition = map_of_elements[element_key]
    
    element_name = element_definition.name
    class_type_definition = element_definition.class_type
    enum_definition = element_definition.enum
    element_comment = element_definition.comment
    element_exportable = element_definition.exportable

    element_text = _create_comment(element_comment)
    if(element_exportable):
        element_text = element_text + 'export '

    if(class_type_definition!=None):
        element_text = element_text + _ts_text_of_class(element_name, class_type_definition)
    else:
        element_text = element_text + _ts_text_of_enum(enum_definition)
    
    return element_text

def _ts_text_of_class(
    class_name,
    class_type_definition
):
    return 'type ' + class_name + ' = ' + _ts_text_of_type_definition(class_type_definition)

def _ts_text_of_enum(
    enum_definition
): 
    enum_text = _create_comment(enum_definition.comment) + 'enum ' + enum_definition.name + ' {\n'
    
    for option in enum_definition.enum_options:
        option_name = option.name
        option_value = option.value
        option_comment = option.comment

        option_text = _create_comment(option_comment, '  ') + '  '

        option_text = option_text + option_name
        if(option_value!=None):
            option_text = option_text + ' = ' + str(option_value)
        option_text = option_text + ','

        enum_text = enum_text + option_text + '\n'
    
    enum_text = enum_text + '}\n'

    return enum_text

def _ts_text_of_type_definition(type_definition, line_indentation = ''):
    simple_type = type_definition.simple_type
    if(simple_type!=None):
        return _get_ts_simple_type(simple_type)
    
    additional_text = ''
    complex_type_text = '{\n'
    object_fields = type_definition.object_fields
    for object_field in object_fields:
        object_field_enum = object_field.enum
        if(object_field_enum!=None):
            additional_text = additional_text + '\n' + _ts_text_of_enum(object_field_enum)
        object_field_name = object_field.name
        object_field_comment = object_field.comment
        if(object_field_comment != None):
            complex_type_text = complex_type_text + _create_comment(object_field_comment, line_indentation = line_indentation + '  ')
        complex_type_text = complex_type_text + '  ' + line_indentation + object_field_name
        object_field_optional = object_field.optional
        if(object_field_optional):
            complex_type_text = complex_type_text + '?'
        object_field_ts_text_type = ''
        if(object_field_enum!=None):
            object_field_ts_text_type = object_field_enum.name
        else:
            object_field_ts_text_type = _ts_text_of_type_definition(object_field.type_definition, line_indentation = line_indentation + '  ')
        if(object_field_ts_text_type.endswith(';\n')):
            object_field_ts_text_type = object_field_ts_text_type[:-2]
        complex_type_text = complex_type_text + ': ' + object_field_ts_text_type
        object_field_nullable = object_field.nullable
        if(object_field_nullable):
            complex_type_text = complex_type_text + ' | null'
        complex_type_text = complex_type_text + ';\n'
    complex_type_text = complex_type_text + line_indentation + '}'
    
    unions = type_definition.unions
    has_unions = False
    if(unions!=None):
        unions_text_list = []
        for union in unions:
            has_unions = True
            unions_text_list.append(_ts_text_of_type_definition(union, line_indentation = line_indentation + '  '))
        if(len(unions_text_list) <= 1):
            complex_type_text = complex_type_text + ' | ' + unions_text_list[0]
        else:
            complex_type_text = '\n' + line_indentation + '  | ' + complex_type_text + \
                                line_indentation + ' | ' + ('\n' + line_indentation + '  | ').join(unions_text_list)
    intersections = type_definition.intersections
    if(intersections!=None):
        intersections_text_list = []
        for intersection in intersections:
            intersections_text_list.append(_ts_text_of_type_definition(intersection, line_indentation = line_indentation + '  '))

        if(has_unions):
            complex_type_text = '(' + complex_type_text 
    
        if(len(intersections_text_list) <= 1):
            complex_type_text = complex_type_text + ' & ' + intersections_text_list[0]
        else:
            complex_type_text = '\n' + line_indentation + '  & ' + complex_type_text + \
                                line_indentation + ' & ' + ('\n' + line_indentation + '  & ').join(intersections_text_list)

        if(has_unions):
            complex_type_text = complex_type_text + ')' 
    
    complex_type_text = complex_type_text + ';\n'

    complex_type_text = complex_type_text + additional_text
    
    return complex_type_text

def _create_comment(comment, line_indentation = '', line_amount_of_letters = 80):
    if(comment==None):
        return ''
    lines = []
    actual_line = line_indentation + " * "

    for word in comment.split(" "):
        if(len(actual_line) + len(word) < line_amount_of_letters):
            actual_line = actual_line + word + " "
        else:
            lines.append(actual_line)
            actual_line = line_indentation + " * " +  word + " "
    lines.append(actual_line)

    return line_indentation + "/**\n" + '\n'.join(lines) + "\n" + line_indentation + " */\n"

def _get_ts_simple_type(type):
    if(type == reserved_integer or type == reserved_double):
        return 'number'
    elif(type == reserved_boolean):
        return 'boolean'
    elif(type == reserved_date):
        return 'Date'
    elif(type == reserved_string):
        return 'string'
    return type

reserved_integer = 'integer'
reserved_double = 'double'
reserved_boolean = 'boolean'
reserved_date = 'date'
reserved_string = 'string'