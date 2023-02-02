import sys
import os

core_folder_path = os.path.abspath((os.path.dirname(sys.argv[0])))
sys.path.append(core_folder_path + '/synthesis/')

from typescript_synthesis import ts_synthesis_of_class

def synthesis_yaml_definition(yaml_definition):
    ts_text = ''

    yaml_imports = yaml_definition.imports
    if(len(yaml_imports)>0):
        ts_text = ts_text + "import {\n  "+',\n  '.join(yaml_imports)+"\n} from 'index.dart';\n\n"

    map_of_classes = {}
    for class_definition in yaml_definition.classes:
        map_of_classes[class_definition.name] = class_definition
    
    for class_definition in yaml_definition.classes:
        ts_text = ts_text + ts_synthesis_of_class(map_of_classes, class_definition.name)

    return ts_text