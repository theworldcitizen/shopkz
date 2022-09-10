import json
from pprint import pprint


class Readfile:
    def read_file(self):
        with open('/home/zhanerke/PycharmProjects/shopkz/src/crawler/smartphones.json', 'r', encoding='utf-8') as file:
            result = json.load(file)
        return result


obj = Readfile()
res = obj.read_file()
