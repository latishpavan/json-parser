from json_parser import JsonParser

json_string = ''

with open("sample.json") as f:
    for line in f.readlines():
        json_string += line

print(JsonParser().parse(json_string)[0])