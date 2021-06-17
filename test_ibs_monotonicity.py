# -*- coding: utf-8 -*-
import argparse
import os.path

def read_file_for_monotonicity(inputfile):
    correct = True
    readingfile = open (inputfile, "r")
    puzzle = None
    cost_list = []
    for line in readingfile:
        if line[:5] == "File:":
            if not puzzle:
                puzzle = line[5:].strip()
            else:
                currpuzzle = line[5:].strip()
                if currpuzzle != puzzle:
                    puzzle = currpuzzle
                    cost_list = []
        elif line[:5] == "Costs":
            if not cost_list:
               cost_list = list(line.strip())
            else:
                currcost_list = list(line.strip())
                for cost in cost_list:
                    if not cost in currcost_list:
                        print(puzzle)
                        print("Solution was missing.")
                        correct = False
    readingfile.close()
    if correct:
        print("Complete. There was no evidence of non-monotonicity.")

if __name__=='__main__':
    PARSE = argparse.ArgumentParser()
    #creates parser
    PARSE.add_argument("-i", help='input file path (shortened)', type=str)
    arguments = PARSE.parse_args()
    #parses arguments
    if not arguments.i:
        print("No input file was given.")
    else:
        if not os.path.exists("C:/Users/melis/" + 
            "OneDrive/Documents/GitHub/search/" + arguments.i):
        #if file cannot be found
            raise ValueError("File could not be found.")
            #raise Value Error (file could not be found)
        read_file_for_monotonicity(arguments.i)