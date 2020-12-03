import csv
import os, json

class CSVtoDict:

    def __init__(self, input_file, delimiter=None):
        """Initalizes relevant variables.

        Args:
            input_file (str): Input CSV file to be read and turned into a list 
            of python dictionaries.
        """
        self.input_file = input_file  
        self.list_of_dicts = []
        self.attr_list_of_dicts = []
        self.headers = []
        if delimiter:
            self.delimiter = delimiter
        else:
            self.delimiter = "_"

    def execute(self):
        self.columnTitles()
        self.toDict()
        self.adjustVAIT()
        self.conjugationFile()
        self.assignRemoveAttributes()

        # self.removeDupe(self.attr_list_of_dicts)
        self.removeDupe(self.list_of_dicts)

        self.writeOutputs(self.attr_list_of_dicts, self.input_file +"_w_attr_dicts.txt")
        self.writeOutputs(self.list_of_dicts, self.input_file +"_dicts.txt")

        return self.list_of_dicts, self.attr_list_of_dicts

    def columnTitles(self):
        """
        Grabs the column/category titles.
        """
        with open(self.input_file, "r") as f:
            reader = csv.reader(f)
            self.headers = next(reader)

    def conjugationFile(self):
        if not os.path.exists('csv2tree_data/app_json_files'):
            os.makedirs('csv2tree_data/app_json_files')
        output_file = "csv2tree_data/app_json_files/conjugation.json"

        with open(output_file, 'w') as json_file:
            json.dump(self.list_of_dicts, json_file,indent=4)

    def toDict(self):
        """Reads in CSV file and 

        Returns:
            Output File (str): Name of file where dictionary list is written.
            List of Dictionaries (list): List of converted dictionaries (with no duplicates)
        """
        with open(self.input_file, newline='') as csvfile:
            scrape_dict = csv.DictReader(csvfile)
            self.list_of_dicts = [x for x in scrape_dict]
        
    def removeDupe(self, removeFrom):
        """
        Removes duplicate dictionary entries from the list.
        """
        
        return [dict(t) for t in {tuple(d.items()) for d in removeFrom}]
        
    def adjustVAIT(self):
        rmv = []
        addto = []
        for d in self.list_of_dicts:
            if d["verb_type"] == "VAIT":
                rmv.append(d)
                temp_VAI = {key: value[:] for key, value in d.items()}
                temp_VAI['verb_type'] = "VAI"
                temp_VAI['gloss'] = temp_VAI['gloss'].replace('VAIT', 'VAI')
                addto.append(temp_VAI)

                temp_VTA = {key: value[:] for key, value in d.items()}
                temp_VTA['verb_type'] = 'VTA'
                temp_VTA['gloss'] = temp_VTA['gloss'].replace('VAIT','VTA')
                temp_VTA['verb_translation'] += " him/her/it"
                addto.append(temp_VTA)

                temp_VTI = {key: value[:] for key, value in d.items()}
                temp_VTI['verb_type'] = 'VTI'
                temp_VTI['gloss'] = temp_VTI['gloss'].replace('VAIT','VTI')
                temp_VTI['verb_translation'] += " it"
                addto.append(temp_VTI)

        for r in rmv:
            self.list_of_dicts.remove(r)
        for a in addto:
            self.list_of_dicts.append(a)
        
        del rmv, addto

    def writeOutputs(self, outputs, file_name):
        if not os.path.exists('csv2tree_data'):
            os.makedirs('csv2tree_data')
        file_name = 'csv2tree_data/' + file_name
        with open(file_name, 'w') as file:
            for n in outputs:
                s = str(n) + "\n"
                file.write(s)
            file.close()

    def assignRemoveAttributesTitles(self):
        """
        If there are columns in the csv files that are attributes of a larger class, this function will
        appropriately group them in the appropriate dictionary.
        A column is considered an attribute of another column if it's title is of the following structure:
        columnname_attributename
        E.g.verb_translation given that there is a separate column entitled 'verb'.
        """
        primary = set()
        attribute = {}
        for col_name in self.headers:
            if self.delimiter not in col_name:
                primary.add(col_name)

        for col_name in self.headers:
            if self.delimiter in col_name:
                prim_attr = col_name.split(self.delimiter)
                if prim_attr[0] not in primary:
                    print(col_name, "is not a valid column name")

                else:
                    attribute[col_name] = {"primary":prim_attr[0], "attribute":prim_attr[1]}

        return primary, attribute

    def assignRemoveAttributes(self):
        """
        Attributes of the primary categories are redundant in the final tree. They should be removed before the tree is made.
        """
        primary, attribute = self.assignRemoveAttributesTitles()
        temp_dicts_list = []
        for col in self.list_of_dicts:
            no_attr = {}
            attr = {}
            for x in col:
                
                if x in primary:
                    no_attr[x] = col[x]
                    attr[x] = {}
                    attr[x]["id"] = col[x]

                if x in attribute:
                    if not attr[attribute[x]["primary"]]:
                        attr[attribute[x]["primary"]] = {}
                    attr[attribute[x]["primary"]][attribute[x]["attribute"]] = col[x]

            temp_dicts_list.append(no_attr)
            self.attr_list_of_dicts.append(attr)
        self.list_of_dicts = temp_dicts_list

