# -*- coding: utf-8 -*-
"""
Algorithm

Created on Wed May 26 19:53:15 2021

"""
import os.path

import argparse

from heap import Heap

class Node:
    
    def __init__(self, state, g, parent, data):
        self.state = state
        self.h = state.heuristic(data)
        self.g = g
        self.f = g + self.h
        self.parent = parent
        
    def __lt__ (self, b):
        return self.f < b.f or (self.f == b.f and self.h < b.h)
        
    def __gt__ (self, b):
        return self.f > b.f or (self.f == b.f and self.h > b.h)
        
    def __eq__ (self, b):
        return self.state.key() == b.state.key()
        
    def __hash__ (self):
        return hash(str(self.state.key()))  
    
    def return_key (self):
        return str(self.state.key())
    
    def print_backwards_path (self):
        self.state.print_information()
        if not self.parent:
            return
        self.parent.print_backwards_path()
        
    def print_path (self, thelist):
        self.collect_path (thelist)
        print("Directions:")
        for i in range(len(thelist)):
            index = -1 * (i + 1)
            if thelist[index] == "l":
                print ("left")
            if thelist[index] == "r":
                print ("right")
            if thelist[index] == "u":
                print ("up")
            if thelist[index] == "d":
                print ("down")
                
    def print_path_j (self, thelist):
        self.collect_path (thelist)
        print("Directions:")
        for i in range(len(thelist)):
            index = -1 * (i + 1)
            if thelist[index] == "l":
                print ("左")
            if thelist[index] == "r":
                print ("右")
            if thelist[index] == "u":
                print ("上")
            if thelist[index] == "d":
                print ("下")
                
    def print_path_a (self, thelist):
        self.collect_path (thelist)
        print("Directions:")
        for i in range(len(thelist)):
            index = -1 * (i + 1)
            if thelist[index] == "l":
                print ("←")
            if thelist[index] == "r":
                print ("→")
            if thelist[index] == "u":
                print ("↑")
            if thelist[index] == "d":
                print ("↓")
    """    
    def collect_path (self, thelist):
        if not self.state._ntype:
            return
        thelist.append(self.state._ntype)
        self.parent.collect_path(thelist)
    """    
    
def search_algorithm (filename, startstate, data, call_type="standard"):
    initial = Node(startstate, 0, None, data)
    heap = Heap([])
    heap.push(initial)
    current = heap.pop()
    expandcount = 0
    gencount = 0
    while current.state.heuristic(data) != 0:
        expandcount += 1
        childcollect = current.state.create_children (data)
        for child in childcollect:
            c = Node (child, current.g + 1, current, data)
            gencount += 1
            if c not in heap:
                heap.push(c)
        current = heap.pop()
    print("Done!\n" + "g: " + str(current.g) + "\n") 
    print("Nodes expanded: " + str(expandcount))
    print("Nodes generated: " + str(gencount) + "\n")
    if call_type == "pictoral":
        current.state.print_goal(data)
    """
    elif call_type == "path":
        pathlist = []
        current.print_path_a(pathlist)
        #current.print_backwards_path()
    """
     
        
if __name__=='__main__':        
#if called from the terminal
    PARSE = argparse.ArgumentParser()
    #creates parser
    PARSE.add_argument("-i", help='input file path (shortened)', type=str)
    PARSE.add_argument("-d", help='domain name in lowercase', type=str)
    PARSE.add_argument("-c", help='call type', type=str)
    arguments = PARSE.parse_args()
    #parses arguments
    if not arguments.i:
        filename = "8_puzzles/1542"
        domain = "sliding_tiles"
    else:
        filename = arguments.i
        if not os.path.exists("C:/Users/melis/" + arguments.i):
            raise ValueError("File could not be found.")      
        domain = arguments.d
    if domain == "blocksworld":
        from blocksworld import read_file
    elif domain == "sliding_tiles":
        from slidingtiles import read_file
    data, initstate = read_file("C:/Users/melis/"+ filename)
    if arguments.c:
        search_algorithm(filename, initstate, data, arguments.c)
    else:
        search_algorithm(filename, initstate, data)