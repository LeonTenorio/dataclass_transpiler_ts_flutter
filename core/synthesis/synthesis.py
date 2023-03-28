import sys
import os

core_folder_path = os.path.abspath((os.path.dirname(sys.argv[0])))
sys.path.append(core_folder_path + '/synthesis/')
sys.path.append(core_folder_path + '/utils/')

from typescript_synthesis import ts_synthesis_of_elements
from dart_synthesis import dart_synthesis_of_elements
from general_utils import map_and_join_array, replace_all
from dart_hive_ids_control import DartHiveTypeIds

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
        ts_text = ts_text + "import {\n  "+',\n  '.join(yaml_imports)+"\n} from 'index';\n\n"
        for yaml_import in yaml_imports:
            ts_imports = _add_if_not_in_list(yaml_import, ts_imports)

    exportable_elements = []

    map_of_elements = {}
    for element_definition in yaml_definition.elements:
        map_of_elements[element_definition.name] = element_definition

    dart_hive_type_ids = DartHiveTypeIds(output_folder_path)
    
    for element_definition in yaml_definition.elements:
        ts_text = ts_text + ts_synthesis_of_elements(map_of_elements, element_definition.name)
        dart_text = dart_text + dart_synthesis_of_elements(map_of_elements, element_definition.name, dart_hive_type_ids)

        if(element_definition.exportable):
            exportable_elements.append(element_definition.name)

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
    if('HiveTypeIds.' in dart_text):
        dart_imports = _add_if_not_in_list('./hive_type_ids.dart', dart_imports)
    if(has_dart_class_import):
        dart_imports = _add_if_not_in_list('./index.dart', dart_imports)
    if('json.' in dart_text):
        dart_imports = _add_if_not_in_list('dart:convert', dart_imports)

    dart_text = map_and_join_array(dart_imports, lambda x: "import '" + x + "';", lambda array: '\n'.join(array)) + dart_text

    _save_generated_output_code(dart_text, file_name, 'dart', output_folder_path)
    _save_generated_output_code(ts_text, file_name, 'ts', output_folder_path)

    dart_hive_type_ids.save_hive_type_ids()

    return file_name, exportable_elements

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