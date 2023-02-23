import os
import sys
from utils.yaml_utils import get_yaml_file_list, read_yaml_content
from definition.yaml_definition import YamlDefinition
from synthesis.synthesis import synthesis_yaml_definition

yaml_folder_path = sys.argv[1]
output_folder_path = os.path.join(os.getcwd(), sys.argv[2])

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

for yaml_file in  yaml_files:
    definition = YamlDefinition(yaml_file['filename'], yaml_file['content'])
    ts_text, dart_text = synthesis_yaml_definition(definition, output_folder_path)