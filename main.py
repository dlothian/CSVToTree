from tree_builder import TreeBuilder
from csv_to_dict import CSVtoDict
from option_builder import OptionBuilder
import sys


def main():

    output_file = "conjugation_tree.json"
    tree_order = None

    if len(sys.argv) == 1:
        print("Please include required input file")
        exit()
    if len(sys.argv) >= 2:
        try:
            f = open(sys.argv[1], 'r')
            f.close()
        except OSError:
            print("Input file '", sys.argv[1], "' not found")
            exit()
        input_file = sys.argv[1]
        if not input_file.endswith(".csv"):
            print("Input file must be a comma separated file and have the .csv extension")
            exit()
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
        if not output_file.endswith(".json"):
            print("Selected output file must be a json file (i.e. must have the .json extension)")
            exit()

    if len(sys.argv) == 4:
        tree_order = sys.argv[3]
        if not tree_order.endswith(".csv"):
            print("Selected tree order file must be a csv file (i.e. must have the .csv extension)")
            exit()
        try:
            f = open(tree_order, 'r')
            f.close()
        except OSError:
            print("Tree order file '", tree_order, "' not found")
            exit()
    
        tree_order_file = open(tree_order, 'r')
        tree_order = tree_order_file.readline().split(',')

    c2d = CSVtoDict(input_file)
    dict_list, attr_dict_list = c2d.execute()
    tb = TreeBuilder(dict_list, output_file, tree_order)
    ob = OptionBuilder(attr_dict_list, tree_order)



if __name__ == "__main__":
    main()