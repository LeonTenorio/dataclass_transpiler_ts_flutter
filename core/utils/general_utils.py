def map_array(array, map_function):
    result = []
    for item in array:
        result.append(map_function(item))
    return result

def map_and_join_array(array, map_function, join_function):
    return join_function(map_array(array, map_function))

def nullable_text(element):
    if(element==None):
        return '-'
    return str(element)

def nullable_element_function(element, nullable_function, not_nullable_function):
    if(element==None):
        return nullable_function()
    else:
        return not_nullable_function(element)

def reduce_array(array, reduce_two_elements):
    result = None
    for element in array:
        if(result==None):
            result = element
        else:
            result = reduce_two_elements(result, element)
    return result

def replace_all(source, expression, new_value):
    return new_value.join(source.split(expression))

def low_case_first_letter(text):
    return text[0].lower() + text[1:]