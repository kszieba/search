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

def generate_csv(algorithm, domain, depth, folder, start, tail):
    if algorithm == "ibs":
        aname = "ibs"
    elif algorithm == "ibs_fcl":
        aname = "ibs_full_closed_list_variant"   
    elif algorithm == "ibs_k":
        aname = "ibs_katrina" 
    else:
        aname = "ibs_katrina_full_closed_list" 
    beams = (10, 20, 40, 60, 80, 100)
    finalname = "_".join([folder, str(start), str(tail), algorithm, str(depth) + ".csv"])
    finalfile = open("New_Results/" + finalname, "w")
    for i in range(start, tail + 1):
        for k in range(6):
            rname = "_".join([algorithm, folder, str(i), str(beams[k]), str(depth) + ".txt"])
            rfile = open("New_Results/Single_Results/" + rname, "r")
                #print(rname, file=sys.stderr)
            data, initstate = read_file("C:/Users/melis/" + folder + "/" + str(i))
            print(",".join([folder, str(i), str(data), rname, aname, str(beams[k]), str(depth), domain]), end=",", file=finalfile)
            count = -1
            collect = ""
            correct = False
            lines_to_keep = (4, 6, 9, 10, 11, 12, 13, 14, 15)
            collected = 0
            for line in rfile:
                count += 1 #count has the right numbers
                #print(count, file=sys.stderr)
                """
                if i == 1:
                    print(i, " ", beams[k], collected, lines_to_keep[collected], count, file=sys.stderr)
                """
                if collected == 9:
                    print("", file=finalfile)
                    #print(i, " ", beams[k], file=sys.stderr)
                    #only executing for the last file
                    break
                elif count == lines_to_keep[collected]:
                    #except for file 4, executing only when count == 4
                    for j in range(len(line)):
                        """
                        if i == 1:
                            print(i, " ", beams[k], count, line[j-1], file=sys.stderr)
                        """
                        if line[j-1] == ":":
                            correct = True
                            continue
                        if correct:
                            if line[j].isnumeric():
                                collect += line[j]
                            elif line[j] == "\n":
                                print(collect, end=",", file=finalfile) #only five printed in the file
                                correct = False
                                collected += 1
                                collect = ""
                                break
            rfile.close()
            #print("Finished reading", file=sys.stderr)
    finalfile.close()

if __name__=='__main__':
    PARSE = argparse.ArgumentParser()
    #creates parser
    PARSE.add_argument("-a", help='algorithm', type=str)
    PARSE.add_argument("-d", help='domain name in lowercase', type=str)
    PARSE.add_argument("-b", help='maximum depth', type=int)
    PARSE.add_argument("-f", help='folder with problem set', type=str)
    PARSE.add_argument("-s", help='start of problem set', type=int)
    PARSE.add_argument("-t", help='tail of problem set', type=int)
    args = PARSE.parse_args()
    if args.d == "blocksworld":
        from blocksworld import read_file
    elif args.d == "sliding_tiles":
        from slidingtiles import read_file
    generate_csv(args.a, args.d, args.b, args.f, args.s, args.t)