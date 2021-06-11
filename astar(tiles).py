# -*- coding: utf-8 -*-
"""
Algorithm

Created on Wed May 26 19:53:15 2021

"""
import os.path

from temp2 import read_file

from temp2 import State

from ediHeap import Heap

filename = "10042"

class Node:
    
    def __init__(self, state, g, parent):
        self.state = state
        self.h = state.heuristic()
        self.g = g
        self.f = g + self.h
        self.parent = parent
        
    def __le__ (self, b):
        return self.f < b.f or self.f == b.f
        
    def __gt__ (self, b):
        return self.f > b.f
        
    def __eq__ (self, b):
        return self.state._locationlist == b.state._locationlist
        
    def __hash__ (self):
        return hash(str(self.state._locationlist[1:]))  
    
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
        
    def collect_path (self, thelist):
        if not self.state._ntype:
            return
        thelist.append(self.state._ntype)
        self.parent.collect_path(thelist)
        
    
def search_algorithm (startstate):
    initial = Node(startstate, 0, None)
    heap = Heap([])
    heap.push(initial)
    current = heap.pop()
    #closedHeap = Heap([])
    expandcount = 0
    gencount =0
    #print(initstate._locationlist)
    while current.state.heuristic() != 0:
        expandcount += 1
        childcollect = current.state.create_children ()
        for child in childcollect:
            c = Node (child, current.g + 1, current)
            if c not in heap.alist:
                gencount += 1
                heap.push(c)
        #closedHeap.push(current)
        current = heap.pop()
    print("Done!\n" + "g: " + str(current.g) + "\n") 
    print("Nodes expanded: " + str(expandcount))
    print("Nodes generated: " + str(gencount) + "\n")
    pathlist = []
    current.print_path_a(pathlist)
    #current.print_backwards_path()
    
     
        
if __name__=='__main__':        
#if called from the terminal
    if os.path.exists("C:/Users/melis/8_puzzles/8_puzzles/"+filename):
        dimens, locations = read_file("C:/Users/melis/8_puzzles/8_puzzles/"+filename)
        initstate = State (dimens, locations)
        #initstate._locationlist = [4, 2, 0, 3, 5, 1, 6, 7, 8]
        #initstate._locationlist = [3, 1, 2, 0, 4, 5, 6, 7, 8]
        #initstate._0location = 2
        #initstate._0location = 3
        search_algorithm(initstate)