import json
from pprint import pprint

with open('smartphones.json') as json_file:
    res = json.load(json_file)
    pprint(res)
