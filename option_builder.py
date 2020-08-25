import json
import os

class OptionBuilder:

    def __init__(self, dict_list):
        """Class creates individual JSON files containing all elements of the individual options, 
        with no duplicates

        Args:
            dict_list (list): List of dictionaries 
        """

        self.dict_list = dict_list
        self.attrs = {}
        self.removeDupes()
        self.writeAttr()


    def removeDupes(self):
        """
        Removes duplicates by adding each element to its respective dictionary attr set
        """
        for key in self.dict_list[0].keys():
            self.attrs[key] = set()

        for d in self.dict_list:
            for attr in d:
                self.attrs[attr].add(d[attr])


    def writeAttr(self):
        """
        Creates each file using the attr dictionary where each key has a set of unique values.
        Files are saved to the 'data' folder.
        """
        if not os.path.exists('data'):
            os.makedirs('data')
        for attr in self.attrs:
            output_file = "data/" + attr + ".json"
            tojson = []
            for value in self.attrs[attr]:
                temp = {"tag":value}
                tojson.append(temp)

            with open(output_file, 'w') as json_file:
                json.dump(tojson, json_file,indent=4, sort_keys=True)
