# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 11:26:35 2021

"-a", help='algorithm', type=str
"-d", help='domain name in lowercase', type=str
"-b", help='maximum depth', type=int
"-f", help='folder with problem set', type=str
"-s", help='start of problem set', type=int
"-t", help='tail of problem set', type=int
"""

import argparse
import os.path
import cProfile
import sys

def separate_into_instances (inputname, beamnumber):
    namelis = inputname.split("beam_set")
    stdout = sys.stdout
    wnames = []
    rfile = open("New_Results/" + inputname, "r")
    resultcount = 0
        #print(rname, file=sys.stderr)
    count = -1
    collect = ""
    correct = False
    lines_to_track = (1, 15)
    
    found = 0
    for line in rfile:
        count += 1 #count has the right numbers
        #print(count, file=sys.stderr)
        if count == 0:
            line1 = line
        elif found == 2:
            resultcount += 1
            wfile.close()
            if resultcount == beamnumber:
                break
            found = 0
            count = -1
            continue
        elif count == lines_to_track[found]:
            for j in range(len(line)):
                if line[j-1] == ":":
                    correct = True
                    continue
                if correct:
                    if line[j].isnumeric():
                        collect += line[j]
                    elif line[j] == "\n":
                        if found == 0:
                            wname = namelis[0] + collect + namelis[1]
                            wfile = open("New_Results/Single_Results/" + wname, "w")
                            sys.stdout = wfile
                            print(line1, end="")
                        print(line)
                        correct = False
                        found += 1
                        collect = ""
                        break
        else:
            print(line, end="")
        #print("Finished reading", file=sys.stderr)
    rfile.close()
    sys.stdout = stdout

if __name__=='__main__':
    PARSE = argparse.ArgumentParser()
    PARSE.add_argument("-i", help='beam set input file', type=str)
    PARSE.add_argument("-n", help='beam number', type=int)
    args = PARSE.parse_args()
    separate_into_instances(args.i, args.n)