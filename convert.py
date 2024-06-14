import ast

# String representation of the list
string_representation = '[-1002186586227, -1002161323205, -1002161323205]'

# Convert the string to a list using ast.literal_eval
list_representation = ast.literal_eval(string_representation)

# Output the converted list
print(list_representation)  # Output: [-1002186586227, -1002161323205]
print(type(list_representation))  # Output: <class 'list'>

for item in list_representation:
    print(item)