# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 14:35:55 2021

This program is intended to test ibs search algorithms of various sorts. It
can run tests utilizing the sliding tiles and blocksworld domains.

The optional arguments it can take are as follows:

-a (algorithm file)
-s (size of test to be conducted) default small (large)
-t (type of test to be conducted) default general (fixed_beam, fixed_depth)
-p (parameter for type of test chosen) default None
-d (domain type in lowercase) default None (sliding_tiles, blocksworld)

"""

import argparse

import os.path

import slidingtiles

import blocksworld
            
def test_algorithm(algorithm, size, giventype, parameter, domain):
    algor = __import__(algorithm)
    beamstart = 20
    beamstop = 61
    depthstart = 70
    depthstop = 101
    if size == "large": 
        filestep1 = 20 
        nameset = ("4puzzle1", "9puzzle2", "12puzzle1", "15puzzle2", "18puzzle1")
        filestop3 = 26
    elif size == "small":
        filestep1 = 30
        nameset = ("4puzzle1", "9puzzle2", "18puzzle1")
        filestop3 = 21
    if giventype == "fixed_beam":
        beamstart = parameter
        beamstop = parameter + 1
    elif giventype == "fixed_depth":
        depthstart = parameter
        depthstop = parameter + 1
        if domain == "sliding_tiles" or domain == None:
            print("Hello")
            for i in range(1, 101, filestep1):
                data, initstate = slidingtiles.read_file("C:/Users/melis/korf100/" + str(i))
                filename = "korf100/" + str(i)
                for beam in range(beamstart, beamstop, 20):
                    for depth in range(depthstart, depthstop, 10):
                        algor.search_algorithm(filename, initstate, data, beam, depth)
        if domain == "blocksworld" or domain == None:
            for name in nameset:
                data, initstate = blocksworld.read_file("C:/Users/melis/blocksworld_puzzles/blocks" + name +".txt")
                filename = "Blocks_world_puzzles/" + name
                for beam in range(beamstart, beamstop, 20):
                    for depth in range(depthstart, depthstop, 10):
                        algor.search_algorithm(filename, initstate, data, beam, depth)
        if domain == "sliding_tiles" or domain == None:
            for i in range(5, filestop3, 5):
                data, initstate = slidingtiles.read_file("C:/Users/melis/8_puzzles/" + str(i) +"42")
                filename = "8_puzzles/" + str(i) + "42"
                for beam in range(beamstart, beamstop, 20):
                    for depth in range(depthstart, depthstop, 10):
                        algor.search_algorithm(filename, initstate, data, beam, depth)
            
if __name__=='__main__':
    PARSE = argparse.ArgumentParser()
    #creates parser
    PARSE.add_argument("-a", help='algorithm file', type=str, required=False)
    PARSE.add_argument("-s", help='size of test to be conducted', type=str, required=False)
    PARSE.add_argument("-t", help='type of test to be conducted', type=str, required=False)
    PARSE.add_argument("-p", help='parameter for type of test chosen', type=int, required=False)
    PARSE.add_argument("-d", help='domain type in lowercase', type=str, required=False)
    arguments = PARSE.parse_args()
    #parses arguments
    algorithm = "ibs_katrina"
    size = "small"
    giventype = "general"
    parameter = None
    domain = None
    if arguments.a:
        algorithm = arguments.a
        #if not os.path.exists(arguments.a):
        #if file cannot be found
            #raise ValueError("File could not be found.")
            #raise Value Error (file could not be found)
    if arguments.s:
        size = arguments.s
    if arguments.t:
        giventype = arguments.t
    if arguments.p:
        parameter = arguments.p
    if arguments.d:
        domain = arguments.d
    test_algorithm (algorithm, size, giventype, parameter, domain) 