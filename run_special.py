# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 23:09:50 2021

@author: melis
"""

"""
Created on Thu Jun 17 13:22:33 2021

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

def run_experiments(algorithm, domain, depth, folder, start, tail, environ="normal"):
    beams = (10, 20, 40, 60, 80, 100)
    beamlen = len(beams)
    if algorithm == "ibs":
        aname = "ibs"
    elif algorithm == "ibs_fcl":
        aname = "ibs_full_closed_list_variant"   
    elif algorithm == "ibs_k":
        aname = "ibs_katrina" 
    elif algorithm == "ibs_kfcl":
        aname = "ibs_katrina_full_closed_list" 
    else:
        aname = "ibs_katrina_max_depth_only"
    algor_file = __import__(aname)
    stdout = sys.stdout
    for i in range(start, tail + 1):
        if environ == "normal":
            data, initstate = read_file("C:/Users/melis/" + folder + "/" + str(i))
        else:
            data, initstate = read_file(folder + "/" + str(i))
        filepath = folder + "/" + str(i)
        for j in range(beamlen):
            wname = "_".join([algorithm, folder, str(i), str(beams[j]), str(depth) + ".txt"])
            wfile = open("New_Results/Single_Results/" + wname, "w")
            sys.stdout = wfile
            algor_file.search_algorithm(filepath, initstate, data, beams[j], depth)
            wfile.close()
    sys.stdout = stdout

if __name__=='__main__':
    PARSE = argparse.ArgumentParser()
    #creates parser
    PARSE.add_argument("-a", help='algorithm', type=str)
    PARSE.add_argument("-k", help='algorithm2', type=str)
    PARSE.add_argument("-d", help='domain name in lowercase', type=str)
    PARSE.add_argument("-b", help='maximum depth', type=int)
    PARSE.add_argument("-f", help='folder with problem set', type=str)
    PARSE.add_argument("-s", help='start of problem set', type=int)
    PARSE.add_argument("-t", help='tail of problem set', type=int)
    PARSE.add_argument("-z", help='start of problem set 2', type=int)
    PARSE.add_argument("-c", help='tail of problem set 2', type=int)
    PARSE.add_argument("-e", help='environment in which program is run', type=str, required=False)
    args = PARSE.parse_args()
    if args.d == "blocksworld":
        from blocksworld import read_file
    elif args.d == "sliding_tiles":
        from slidingtiles import read_file
    if not args.e:
        run_experiments(args.a, args.d, args.b, args.f, args.s, args.t)
        run_experiments(args.k, args.d, args.b, args.f, args.z, args.c)
    else:
        run_experiments(args.a, args.d, args.b, args.f, args.s, args.t, args.e)
        run_experiments(args.k, args.d, args.b, args.f, args.z, args.c, args.e)