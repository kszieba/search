# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 14:35:55 2021

@author: melis
"""

import argparse

import os.path

import slidingtiles

import blocksworld

"""
for i in range(1, 101, 20):
    data, initstate = slidingtiles.read_file("C:/Users/melis/korf100/" + str(i))
    filename = "korf100/" + str(i)
    for beam in range(20, 61, 20):
        for depth in range(70, 101, 10):
            search_algorithm(filename, initstate, data, beam, depth)

for name in ("4puzzle1", "9puzzle2", "12puzzle1", "15puzzle2", "18puzzle1"):
    data, initstate = blocksworld.read_file("C:/Users/melis/blocksworld_puzzles/blocks" + name +".txt")
    filename = "Blocks_world_puzzles/" + name
    for beam in range(20, 61, 20):
        for depth in range(70, 101, 10):
            search_algorithm(filename, initstate, data, beam, depth)
for i in range(5, 30, 5):
    data, initstate = slidingtiles.read_file("C:/Users/melis/8_puzzles/" + str(i) +"42")
    filename = "8_puzzles/" + str(i) + "42"
    for beam in range(20, 60, 20):
        for depth in range(70, 100, 10):
            search_algorithm(filename, initstate, data, beam, depth)
"""
            
def test_algorithm(algorithm, size, giventype, parameter, domain):
    algor = __import__(algorithm)
    if size == "large": 
        filestep1 = 20 
        nameset = ("4puzzle1", "9puzzle2", "12puzzle1", "15puzzle2", "18puzzle1")
        stop3 = 26
    elif size == "small":
        filestep1 = 30
        nameset = ("4puzzle1", "9puzzle2", "18puzzle1")
        stop3 = 21
    if giventype == "general":
        if domain == "sliding_tiles" or domain == None:
            print("Hello")
            for i in range(1, 101, filestep1):
                data, initstate = slidingtiles.read_file("C:/Users/melis/korf100/" + str(i))
                filename = "korf100/" + str(i)
                for beam in range(20, 61, 20):
                    for depth in range(70, 101, 10):
                        algor.search_algorithm(filename, initstate, data, beam, depth)
        if domain == "blocksworld" or domain == None:
            for name in nameset:
                data, initstate = blocksworld.read_file("C:/Users/melis/blocksworld_puzzles/blocks" + name +".txt")
                filename = "Blocks_world_puzzles/" + name
                for beam in range(20, 61, 20):
                    for depth in range(70, 101, 10):
                        algor.search_algorithm(filename, initstate, data, beam, depth)
        if domain == "sliding_tiles" or domain == None:
            for i in range(5, stop3, 5):
                data, initstate = slidingtiles.read_file("C:/Users/melis/8_puzzles/" + str(i) +"42")
                filename = "8_puzzles/" + str(i) + "42"
                for beam in range(20, 61, 20):
                    for depth in range(70, 100, 10):
                        algor.search_algorithm(filename, initstate, data, beam, depth)
    if giventype == "fixed_beam":
        beam =  parameter
        if domain == "sliding_tiles" or domain == None:
            for i in range(1, 101, filestep1):
                data, initstate = slidingtiles.read_file("C:/Users/melis/korf100/" + str(i))
                filename = "korf100/" + str(i)
                for depth in range(70, 101, 10):
                    algor.search_algorithm(filename, initstate, data, beam, depth)
        if domain == "blocksworld" or domain == None:
            for name in nameset:
                data, initstate = blocksworld.read_file("C:/Users/melis/blocksworld_puzzles/blocks" + name +".txt")
                filename = "Blocks_world_puzzles/" + name
                for depth in range(70, 101, 10):
                    algor.search_algorithm(filename, initstate, data, beam, depth)
        if domain == "sliding_tiles" or domain == None:
            for i in range(5, stop3, 5):
                data, initstate = slidingtiles.read_file("C:/Users/melis/8_puzzles/" + str(i) +"42")
                filename = "8_puzzles/" + str(i) + "42"
                for depth in range(70, 101, 10):
                    algor.search_algorithm(filename, initstate, data, beam, depth)
    if giventype == "fixed_depth":
        depth = parameter
        if domain == "sliding_tiles" or domain == None:
            for i in range(1, 101, filestep1):
                data, initstate = slidingtiles.read_file("C:/Users/melis/korf100/" + str(i))
                filename = "korf100/" + str(i)
                for beam in range(20, 61, 20):
                    algor.search_algorithm(filename, initstate, data, beam, depth)
        if domain == "blocksworld" or domain == None:
            for name in nameset:
                data, initstate = blocksworld.read_file("C:/Users/melis/blocksworld_puzzles/blocks" + name +".txt")
                filename = "Blocks_world_puzzles/" + name
                for beam in range(20, 61, 20):
                    algor.search_algorithm(filename, initstate, data, beam, depth)
        if domain == "sliding_tiles" or domain == None:
            for i in range(5, stop3, 5):
                data, initstate = slidingtiles.read_file("C:/Users/melis/8_puzzles/" + str(i) +"42")
                filename = "8_puzzles/" + str(i) + "42"
                for beam in range(20, 61, 20):
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