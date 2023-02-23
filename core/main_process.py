import os
import sys
import subprocess
from utils.yaml_utils import get_yaml_file_list, read_yaml_content
from definition.yaml_definition import YamlDefinition
from synthesis.synthesis import synthesis_yaml_definition
from utils.general_utils import map_and_join_array

yaml_folder_path = sys.argv[1]
output_folder_path = os.path.join(os.getcwd(), (sys.argv[2]).replace("./", ""))

core_folder_path = os.path.abspath((os.path.dirname(sys.argv[0])))

# Go to yaml definition folder and get the yaml files content
os.chdir(yaml_folder_path)
yaml_file_list = get_yaml_file_list()

yaml_files = []
for file in yaml_file_list:
    yaml_files.append({
        'filename': file,
        'content': read_yaml_content(file)
    })

# Back to core folder to execute the other files
os.chdir(core_folder_path)

dart_index_file_text = "export './include_in_output/date_time_converter.dart';\n" + \
                       "export './include_in_output/models_box.dart';\n"
ts_index_file_text = ''

subprocess.Popen("cp -R '" + os.path.join(os.getcwd(), "include_in_output/") + "' '" + output_folder_path[:-1] + "'", shell=True)

for yaml_file in  yaml_files:
    definition = YamlDefinition(yaml_file['filename'], yaml_file['content'])
    generated_file_name, generated_exported_items = synthesis_yaml_definition(definition, output_folder_path)
    if(len(generated_exported_items) > 0):
        dart_index_file_text = dart_index_file_text + "export './" + generated_file_name + ".dart';\n"
        ts_index_file_text = ts_index_file_text + "export {\n" + map_and_join_array(
            generated_exported_items, 
            lambda x: '  ' + x + ',',
            lambda array: '\n'.join(array)
        ) + "\n} from './" + generated_file_name + ".ts';\n"

with open(output_folder_path + "/index.dart", "w") as f:
    f.write(dart_index_file_text)
with open(output_folder_path + "/index.ts", "w") as f:
    f.write(ts_index_file_text)