import json
import os
import sys

class OptionBuilder:

    def __init__(self, attr_dict_list, data_order):
        """Class creates individual JSON files containing all elements of the individual options, 
        with no duplicates

        Args:
            dict_list (list): List of dictionaries 
        """

        self.attr_dict_list = attr_dict_list
        self.attrs = {}
        self.data_order = data_order
        self.removeDupes()
        self.writeAttr()


    def orderAttrs(self):
        """
        If tree order is given, data should be ordered in the same way.
        """


    def removeDupes(self):
        """
        Removes duplicates by adding each element to its respective dictionary attr set
        """
        if self.data_order:
            for key in self.data_order:
                self.attrs[key] = set()
        else:
            for key in self.attr_dict_list[0].keys():
                self.attrs[key] = set()

        for d in self.attr_dict_list:
            for attr in d:
                self.attrs[attr].add(tuple(d[attr].items()))

        for key in self.attrs:
            temp = [dict(t) for t in self.attrs[key]]
            self.attrs[key] = temp
        

    def writeAttr(self):
        """
        Creates each file using the attr dictionary where each key has a set of unique values.
        Files are saved to the 'data' folder.
        """
        if not os.path.exists('csv2tree_data/app_json_files'):
            os.makedirs('csv2tree_data/app_json_files')
        major_output_file = "csv2tree_data/app_json_files/information.json"
        major = []
        for attr in self.attrs:
            output_file = "csv2tree_data/app_json_files/" + attr + ".json"
            tojson = {"name":attr, "children":[]}
            for value in self.attrs[attr]:
                tojson["children"].append(value)
            newlist = sorted(tojson["children"], key=lambda k: k['id']) 
            tojson["children"] = newlist

            with open(output_file, 'w') as json_file:
                json.dump(tojson, json_file,indent=4)
            major.append(tojson)

        with open(major_output_file, 'w') as json_file:
            json.dump(major, json_file,indent=4)