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

def create_beam_set(algorithm, domain, depth, folder, start, tail):
    beams = (10, 20, 40, 60, 80, 100)
    beamlen = len(beams)
    for i in range(start, tail + 1):
        finalname = "_".join([algorithm, folder, str(i), "beam_set", str(depth) + ".txt"])
        finalfile = open("New_Results/Beam_Set_Files/" + finalname, "w")
        for k in range(beamlen):
            rname = "_".join([algorithm, folder, str(i), str(beams[k]), str(depth) + ".txt"])
            rfile = open("New_Results/Single_Results/" + rname, "r")
                #print(rname, file=sys.stderr)
            data, initstate = read_file("C:/Users/melis/" + folder + "/" + str(i))
            count = -1
            for line in rfile:
                count += 1 #count has the right numbers
                #print(count, file=sys.stderr)
                print(line, end="", file=finalfile)
                if count == 16:
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
    create_beam_set(args.a, args.d, args.b, args.f, args.s, args.t)