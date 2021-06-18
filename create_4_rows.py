# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 13:22:33 2021

@author: melis
"""
import argparse
import os.path
import cProfile
import sys

import ibs
import ibs_full_closed_list_variant
import ibs_katrina
import ibs_katrina_full_closed_list

def create_4_rows(inputpath, domain, beam, depth):
    path = inputpath.split("/")
    folder = path[0]
    file = path[1]
    stdout = sys.stdout
    data, initstate = read_file("C:/Users/melis/" + folder + "/" + file)
    wnames = []
    #algorithms = ("ibs", "ibs_fcl")
    algorithms = ("ibs", "ibs_fcl", "ibs_k", "ibs_kfcl")
    for algorithm in algorithms:
        wname = "_".join([algorithm, folder, file, str(beam), str(depth) + ".txt"])
        wnames.append(wname)
        wfile = open("Testing_Results/" + wname, "w")
        sys.stdout = wfile
        if algorithm == "ibs":
            cProfile.runctx("ibs.search_algorithm(file, initstate, data, beam, depth)", 
    {"ibs": ibs, "file": file, "initstate": initstate, "data": data, "beam": beam, 
     "depth": depth}, {})
        elif algorithm == "ibs_fcl":
            cProfile.runctx("ibs_full_closed_list_variant.search_algorithm(file, initstate, data, beam, depth)", 
    {"ibs_full_closed_list_variant" : ibs_full_closed_list_variant, "file": file, "initstate": initstate, "data": data, "beam": beam, 
     "depth": depth}, {})
        elif algorithm == "ibs_k":
            cProfile.runctx("ibs_katrina.search_algorithm(file, initstate, data, beam, depth)", 
    {"ibs_katrina": ibs_katrina, "file": file, "initstate": initstate, "data": data, "beam": beam, 
     "depth": depth}, {})
        elif algorithm == "ibs_kfcl":
            cProfile.runctx("ibs_katrina_full_closed_list.search_algorithm(file, initstate, data, beam, depth)", 
    {"ibs_katrina_full_closed_list": ibs_katrina_full_closed_list, "file": file, "initstate": initstate, "data": data, "beam": beam, 
     "depth": depth}, {})
        wfile.close()
    finalname = "_".join([folder, file, str(beam), str(depth) + ".csv"])
    finalfile = open(finalname, "w")
    sys.stdout = finalfile
    for i in range(len(algorithms)):
        algorithm = algorithms[i]
        rname = wnames[i]
        rfile = open("Testing_Results/" + rname, "r")
        count = -1
        time = ""
        g = ""
        gcount = ""
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
                for k in range(len(line)):
                    if line[k-1] == ":":
                        correct = True
                        continue
                    if correct:
                        if line[k].isnumeric():
                            gcount += line[k]
                        elif line[k] == "\n":
                            #print(gcount, file=sys.stderr)
                            correct = False
                            break
            elif count == 12:
                #print(line, file=sys.stderr, end="")
                for l in range(len(line)):
                    if line[l-2:l] == "in":
                        correct = True
                        continue
                    if correct:
                        if line[l].isnumeric() or line[l] == ".":
                            time += line[l]
                        elif line[l] == "\n":
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
        print(",".join([wnames[i], aname, domain, folder, file, str(data), str(beam), str(depth), g, gcount, time]))
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
    create_4_rows (arguments.i, arguments.d, arguments.w, arguments.b)