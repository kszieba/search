# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 11:51:55 2021

@author: melis
"""

import argparse
import sys

def read_files_for_csv(inputpath, domain, beam, depth):
    path = inputpath.split("/")
    folder = path[0]
    file = path[1]
    stdout = sys.stdout
    data, initstate = read_file("C:/Users/melis/" + folder + "/" + file)
    finalname = "_".join([folder, file, str(beam), str(depth) + "_2.csv"])
    finalfile = open(finalname, "w")
    sys.stdout = finalfile
    algorithms = ("ibs", "ibs_fcl", "ibs_k", "ibs_kfcl")
    for i in range(len(algorithms)):
        algorithm = algorithms[i]
        rname = "_".join([algorithm, folder, file, str(beam), str(depth) + ".txt"])
        rfile = open("Testing_Results/" + rname, "r")
        count = -1
        g = ""
        gcount = ""
        excount = ""
        gencount = ""
        time = ""
        correct = False
        for line in rfile:
            count += 1
            if count == 4:
                #print(line, file=sys.stderr, end="")
                for j in range(len(line)):
                    if line[j-1] == ":":
                        correct = True
                        continue
                    if correct:
                        if line[j].isnumeric():
                            g += line[j]
                        elif line[j] == "\n":
                            #print(g, file=sys.stderr)
                            correct = False
                            break
            elif count == 6:
                #print(line, file=sys.stderr, end="")
                j = 0
                for j in range(len(line)):
                    if line[j-1] == ":":
                        correct = True
                        continue
                    if correct:
                        if line[j].isnumeric():
                            gcount += line[j]
                        elif line[j] == "\n":
                            #print(gcount, file=sys.stderr)
                            correct = False
                            break
            elif count == 9:
                #print(line, file=sys.stderr, end="")
                j = 0
                for j in range(len(line)):
                    if line[j-1] == ":":
                        correct = True
                        continue
                    if correct:
                        if line[j].isnumeric():
                            excount += line[j]
                        elif line[j] == "\n":
                            #print(gcount, file=sys.stderr)
                            correct = False
                            break
            elif count == 10:
                #print(line, file=sys.stderr, end="")
                j = 0
                for j in range(len(line)):
                    if line[j-1] == ":":
                        correct = True
                        continue
                    if correct:
                        if line[j].isnumeric():
                            gencount += line[j]
                        elif line[j] == "\n":
                            #print(gcount, file=sys.stderr)
                            correct = False
                            break
            elif count == 12:
                #print(line, file=sys.stderr, end="")
                j = 0
                for j in range(len(line)):
                    if line[j-2:j] == "in":
                        correct = True
                        continue
                    if correct:
                        if line[j].isnumeric() or line[j] == ".":
                            time += line[j]
                        elif line[j] == "\n":
                            #print(time, file=sys.stderr)
                            correct = False
                            break
            elif count == -1:
                break
        if algorithm == "ibs":
            aname = "ibs"
        elif algorithm == "ibs_fcl":
            aname = "ibs_full_closed_list_variant"   
        elif algorithm == "ibs_k":
            aname = "ibs_katrina" 
        else:
            aname = "ibs_katrina_full_closed_list"  
        print(",".join([rname, aname, domain, folder, file, str(data), 
                        str(beam), str(depth), g, gcount, excount, gencount,
                        time]))
        rfile.close()
    finalfile.close()
    sys.stdout = stdout
    
if __name__=='__main__':
    PARSE = argparse.ArgumentParser()
    #creates parser
    PARSE.add_argument("-i", help='input file path (shortened)', type=str)
    PARSE.add_argument("-d", help='domain name in lowercase', type=str)
    PARSE.add_argument("-w", help='beam width', type=int)
    PARSE.add_argument("-b", help='maximum depth', type=int)
    arguments = PARSE.parse_args()
    if arguments.d == "blocksworld":
        from blocksworld import read_file
    elif arguments.d == "sliding_tiles":
        from slidingtiles import read_file
    read_files_for_csv (arguments.i, arguments.d, arguments.w, arguments.b)