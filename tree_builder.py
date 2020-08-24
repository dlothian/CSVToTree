import itertools
import re
import sys
import json
import sys

class TreeBuilder:

    def __init__(self, input_dict, output_file):
        self.input_dict = input_dict
        self.output_file = output_file
        self.keys = None
        self.toTree()
        
    def toTree(self):

        tree = {}
        self.keys = list(self.input_dict[0].keys())

        print("Your tree will be built with the following structure:")
        for i in range(len(self.keys)):
            print("Level", i, ":", self.keys[i])


        for verb in self.input_dict: # Going through each dictionary in new list
            self.recursiveTree(tree, verb, 0)

        with open(self.output_file, 'w') as json_file:
            json.dump(tree, json_file,indent=4, sort_keys=True)

        return


    def recursiveTree(self, tree, verb, index):
        """[summary]

        Args:
            tree ([type]): [description]
            verb ([type]): [description]
            index ([type]): [description]

        Returns:
            [type]: [description]
        """
                
        if verb[self.keys[index]] not in tree:
            if index == (len(self.keys) - 1):
                tree.append(verb[self.keys[index]])
                return

            elif index == (len(self.keys) - 2):
                tree[verb[self.keys[index]]] = []

            else:
                tree[verb[self.keys[index]]] = {}
         
        self.recursiveTree(tree[verb[self.keys[index]]], verb, index+1)
        
        return 