import itertools
import re
import sys
import json
import sys

class TreeBuilder:

    def __init__(self, input_dict, output_file, keys):
        """Class takes a list of dictionaries and creates a tree data structure through dictionaries.
        Calls tree builder function.

        Args:
            input_dict (list): List of dictionaries
            output_file (str): Tree output file name
            keys (list): List of key names, if user specified
        """
        self.input_dict = input_dict
        self.output_file = output_file
        self.keys = keys
        self.toTree()
        

    def toTree(self):
        """
        Function does the following:
        1. Ensures that the tree order submitted is valud
        2. Calls tree builder function
        3. Writes tree to output file
        """
        tree = {}
        if not self.keys:
            self.keys = list(self.input_dict[0].keys())
        # else:
        #     temp_keys = []
        #     for i in self.keys:
        #         temp_keys.append(i)
        #     temp_keys.sort()
        #     original_keys = list(self.input_dict[0].keys())
        #     original_keys.sort()

        #     if temp_keys != original_keys:
        #         print("Tree order file does not contain valid attribute names")
        #         print("Tree order file attributes must be of the same name as the row headers in input file")
        #         print("Your file's options are", original_keys)
        #         print("Your order attribute names are", temp_keys)
        #         exit()

        print("Your tree will be built with the following structure:")
        for i in range(len(self.keys)):
            print("Level", i, ":", self.keys[i])

        for verb in self.input_dict: # Going through each dictionary in new list
            self.recursiveTree(tree, verb, 0)

        with open(self.output_file, 'w') as json_file:
            json.dump(tree, json_file,indent=4, sort_keys=True)

        return


    def recursiveTree(self, tree, verb, index):
        """
        Recursively creates

        Args:
            tree (dict or list): Tree at different levels, list if it's the last level.
            verb (dict): Dictionary that contains a line from the original csv
            index (int): Index of position of keys array, denoting which level of the tree is current

        Returns:
            [type]: [description]
        """
        
        if verb[self.keys[index]] not in tree: # If this node is not currently at this level, add it
            if index == (len(self.keys) - 1): # if current level is the last level
                tree.append(verb[self.keys[index]]) # add it to the last level list
                return # move on to next verb

            elif index == (len(self.keys) - 2): # else if current level is second last level
                tree[verb[self.keys[index]]] = [] # add it to dictionary with empty list value (i.e. the last level)

            else: # if any other level
                tree[verb[self.keys[index]]] = {} # add it to dictionary with empty dictionary value for the next level.

        if index < (len(self.keys) - 1):
            self.recursiveTree(tree[verb[self.keys[index]]], verb, index+1) #if this node *is* at the current level, check if next node is at next level.
        
        return 
