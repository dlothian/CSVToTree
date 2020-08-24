import json

class OptionBuilder:

    def __init__(self, dict_list):
        self.dict_list = dict_list
        self.attrs = {}
        self.removeDupes()
        self.writeAttr()

    def removeDupes(self):
        for key in self.dict_list[0].keys():
            self.attrs[key] = set()

        for d in self.dict_list:
            for attr in d:
                self.attrs[attr].add(d[attr])


    def writeAttr(self):

        for attr in self.attrs:
            output_file = attr + ".json"
            tojson = []
            for value in self.attrs[attr]:
                temp = {"tag":value}
                tojson.append(temp)

            with open(output_file, 'w') as json_file:
                json.dump(tojson, json_file,indent=4, sort_keys=True)
