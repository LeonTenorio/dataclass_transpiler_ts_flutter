import os 

class DartHiveTypeIds:
    def __init__(self, output_path):
        self.output_path = output_path
        self.map_of_dart_hive_type_id_for_elements = _load_already_saved_hive_type_ids(self.output_path)
    def get_hive_type_id(self, element_name):
        return _get_object_hive_type_id(self.map_of_dart_hive_type_id_for_elements, element_name)
    def save_hive_type_ids(self):
        _save_hive_type_ids(self.map_of_dart_hive_type_id_for_elements, self.output_path)

def _get_output_file_path(path):
    file_path = path + '/hive_type_ids.dart'
    return file_path

def _load_already_saved_hive_type_ids(path):
    file_path = _get_output_file_path(path)

    map_of_dart_hive_type_id_for_elements = {}

    if(os.path.exists(file_path)==False):
        return map_of_dart_hive_type_id_for_elements
    
    with open(file_path, 'r') as f:
        file_content = f.read()
        aux = file_content.split(';\n')
        if(len(aux)>1):
            aux.pop(0)
            aux.pop(len(aux)-1)
            elements_type_id_lines = aux.copy()
            for element_type_id_line in elements_type_id_lines:
                type_id_content = element_type_id_line.split('static const int ')[1]
                aux = type_id_content.split(' = ')
                element_name = aux[0]
                element_index = int(aux[1])

                map_of_dart_hive_type_id_for_elements[element_name] = _DartHiveTypeIdForObject(
                    element_name,
                    element_index,
                    False
                )
    
    return map_of_dart_hive_type_id_for_elements
        
def _get_object_hive_type_id(map_of_dart_hive_type_id_for_elements, element_name):    
    if(element_name in map_of_dart_hive_type_id_for_elements):
        map_of_dart_hive_type_id_for_elements[element_name].set_field_in_use(True)
    else:
        map_of_dart_hive_type_id_for_elements[element_name] = _DartHiveTypeIdForObject(
            element_name, 
            None,
            True
        )
    
    return "HiveTypeIds." + element_name

def _save_hive_type_ids(map_of_dart_hive_type_id_for_elements, output_path):
    with open(_get_output_file_path(output_path), 'w') as f:
        f.write(_get_hive_type_ids_output_text(map_of_dart_hive_type_id_for_elements))

def _get_hive_type_ids_output_text(map_of_dart_hive_type_id_for_elements):
    effective_dart_hive_type_id_list = []
    for dart_hive_type_id_for_element in list(map_of_dart_hive_type_id_for_elements.values()):
        if(dart_hive_type_id_for_element.field_in_use):
            effective_dart_hive_type_id_list.append(dart_hive_type_id_for_element)
    __fill_list_dart_hive_type_id_for_element_index(effective_dart_hive_type_id_list)

    output_text = 'class HiveTypeIds {\n' + \
                  '  HiveTypeIds._();\n'
    for dart_hive_type_id in effective_dart_hive_type_id_list:
        output_text = output_text + '  static const int ' + dart_hive_type_id.name + ' = ' + str(dart_hive_type_id.index) + ';\n'
    output_text = output_text + '}\n'

    return output_text
    
def __fill_list_dart_hive_type_id_for_element_index(list):
    list_length = len(list)
    list.sort(key=lambda x: __sort_dart_hive_type_id_for_element_key(x, list_length))
    
    next_index = 1
    for index, element in enumerate(list):
        if(element.index != None):
            next_index = element.index + 1
        else:
            element.set_index(next_index)
            next_index = next_index + 1
    
    return list

def __get_next_dart_hive_type_id_for_element_index_list_without_index(list, base_index):
    for i in range(base_index, len(list)):
        if(list[i].index == None):
            return i
    return None

def __sort_dart_hive_type_id_for_element_key(element, inf):
    if(element.index == None):
        return inf
    return element.index

class _DartHiveTypeIdForObject:
    def __init__(self, name, index, field_in_use):
        self.name = name
        self.index = index
        self.field_in_use = field_in_use
    def set_index(self, index):
        self.index = index
    def set_field_in_use(self, field_in_use):
        self.field_in_use = field_in_use