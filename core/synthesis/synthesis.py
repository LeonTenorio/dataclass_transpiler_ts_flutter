import sys
import os

core_folder_path = os.path.abspath((os.path.dirname(sys.argv[0])))
sys.path.append(core_folder_path + '/synthesis/')
sys.path.append(core_folder_path + '/utils/')

from typescript_synthesis import ts_synthesis_of_class
from dart_synthesis import dart_synthesis_of_classes
from general_utils import map_and_join_array, replace_all

def synthesis_yaml_definition(yaml_definition, output_folder_path):
    file_name = replace_all(replace_all(yaml_definition.file_name, './', ''), '.yaml', '')
    ts_text = ''
    dart_text = "\n\npart '" + file_name + ".freezed.dart';\n" + \
                "part '" + file_name + ".g.dart';\n\n"

    ts_imports = []
    dart_imports = ['package:freezed_annotation/freezed_annotation.dart']

    has_dart_class_import = len(yaml_definition.imports) > 0

    yaml_imports = yaml_definition.imports
    if(len(yaml_imports)>0):
        ts_text = ts_text + "import {\n  "+',\n  '.join(yaml_imports)+"\n} from 'index.dart';\n\n"
        for yaml_import in yaml_imports:
            ts_imports = _add_if_not_in_list(yaml_import, ts_imports)

    exportable_classes = []

    map_of_classes = {}
    for class_definition in yaml_definition.classes:
        map_of_classes[class_definition.name] = class_definition
    
    for class_definition in yaml_definition.classes:
        ts_text = ts_text + ts_synthesis_of_class(map_of_classes, class_definition.name)
        dart_text = dart_text + dart_synthesis_of_classes(map_of_classes, class_definition.name)

        if(class_definition.exportable):
            exportable_classes.append(class_definition.name)

    if('@Hive' in dart_text):
        dart_imports.append('package:hive_flutter/hive_flutter.dart')
    if('required DateTime ' in dart_text):
        dart_text = replace_all(dart_text, 'required DateTime ', '@DateTimeConverter() required DateTime ')
        dart_imports = _add_if_not_in_list('./core/datetime_converter.dart', dart_imports)
    if('required DateTime? ' in dart_text):
        dart_text = replace_all(dart_text, 'required DateTime? ', '@NullableDateTimeConverter() required DateTime? ')
        dart_imports = _add_if_not_in_list('./core/datetime_converter.dart', dart_imports)
    if('required DateTime ' not in dart_text and 'required DateTime? ' not in dart_text and 'DateTime? ' in dart_text):
        dart_text = replace_all(dart_text, 'DateTime? ', '@NullableDateTimeConverter() DateTime? ')
        dart_imports = _add_if_not_in_list('./core/datetime_converter.dart', dart_imports)
    if('Tuple2' in dart_text):
        dart_imports = _add_if_not_in_list('package:package:dartz/dartz.dart', dart_imports)
    if(has_dart_class_import):
        dart_imports = _add_if_not_in_list('./index.dart', dart_imports)

    dart_text = map_and_join_array(dart_imports, lambda x: "import '" + x + "';", lambda array: '\n'.join(array)) + dart_text

    _save_generated_output_code(dart_text, file_name, 'dart', output_folder_path)
    _save_generated_output_code(ts_text, file_name, 'ts', output_folder_path)

    return file_name, exportable_classes

def _add_if_not_in_list(element, list):
    if(element not in list):
        list.append(element)
    return list

def _save_generated_output_code(generated_text, yaml_file_name, extension, output_folder_path):
    if(os.path.exists(output_folder_path)==False):
        os.mkdir(output_folder_path)

    output_file_name = output_folder_path + yaml_file_name + '.' + extension

    with open(output_file_name, 'w+') as f:
        f.write(generated_text)