# -*- coding: utf-8 -*-
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

def run_experiments(algorithm, domain, depth, folder, start, tail):
    if algorithm == "ibs":
        aname = "ibs"
    elif algorithm == "ibs_fcl":
        aname = "ibs_full_closed_list_variant"   
    elif algorithm == "ibs_k":
        aname = "ibs_katrina" 
    else:
        aname = "ibs_katrina_full_closed_list" 
    algor_file = __import__(aname)
    stdout = sys.stdout
    wnames = []
    for i in range(start, tail + 1):
        data, initstate = read_file("C:/Users/melis/" + folder + "/" + str(i))
        wname = "_".join([algorithm, folder, str(i), "beam_set", str(depth) + ".txt"])
        wnames.append(wname)
        beams = (10, 20, 40, 60, 80, 100)
        filepath = folder + "/" + str(i)
        wfile = open("New_Results/" + wname, "w")
        sys.stdout = wfile
        for j in range(6):
            """
            print(j, file=sys.stderr)
            print(beams[j], file=sys.stderr)
            """
            algor_file.search_algorithm(filepath, initstate, data, beams[j], depth)
        wfile.close()
    finalname = "_".join([folder, str(start), str(tail), algorithm, str(depth) + ".csv"])
    finalfile = open(finalname, "w")
    sys.stdout = finalfile
    for i in range(start, tail + 1):
        rname = wnames[i - start]
        rfile = open("New_Results/" + rname, "r")
        resultcount = 0
            #print(rname, file=sys.stderr)
        print(",".join([folder, str(i), str(data), rname, aname, str(beams[resultcount]), str(depth), domain]), end=",")
        count = -1
        collect = ""
        correct = False
        lines_to_keep = (4, 6, 9, 10, 11, 12, 13, 14, 15)
        collected = 0
        for line in rfile:
            count += 1 #count has the right numbers
            #print(count, file=sys.stderr)
            if collected == 9:
                print("")
                resultcount += 1
                if resultcount == 6:
                    break
                collected = 0
                count = -1
                print(",".join([folder, str(i), str(data), rname, aname, str(beams[resultcount]), str(depth), domain]), end=",") #runs five times, as it should
                #print("Hello?", file=sys.stderr)
                continue
            elif count == lines_to_keep[collected]:
                for j in range(len(line)):
                    if line[j-1] == ":":
                        correct = True
                        continue
                    if correct:
                        if line[j].isnumeric():
                            collect += line[j]
                        elif line[j] == "\n":
                            print(collect, end=",") #only five printed in the file
                            """
                            if lines_to_keep[k]==6:
                                print(collect, file=sys.stderr) #six here, correct
                            """
                            correct = False
                            collected += 1
                            collect = ""
                            break
        rfile.close()
        #print("Finished reading", file=sys.stderr)
    finalfile.close()
    sys.stdout = stdout

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
    run_experiments(args.a, args.d, args.b, args.f, args.s, args.t)