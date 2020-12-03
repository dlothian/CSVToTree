import csv
import os

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

