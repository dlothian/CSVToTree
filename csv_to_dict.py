import csv

class CSVtoDict:

    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = input_file[:-4] + "_dict.txt"    
        self.list_of_dicts = None


    def toDict(self):
        with open(self.input_file, newline='') as csvfile:
            scrape_dict = csv.DictReader(csvfile)
            self.list_of_dicts = [x for x in scrape_dict]
        self.removeDupe()

        return self.output_file, self.list_of_dicts
        

        
    def removeDupe(self):
        self.list_of_dicts = [dict(t) for t in {tuple(d.items()) for d in self.list_of_dicts}]
        with open(self.output_file, 'w') as file:
            for n in self.list_of_dicts:
                s = str(n) + "\n"
                file.write(s)
            file.close()