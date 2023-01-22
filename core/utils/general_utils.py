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