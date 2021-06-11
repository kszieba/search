# -*- coding: utf-8 -*-
"""
Incremental Beam Search Algorithm

This version assumes cost is constant and does not explore deeper levels than
the one where the current best solution was found.

Created on Tue Jun  8 13:47:52 2021

"""

import os.path

import argparse

from collections import OrderedDict

from Heap_with_keys import IHeap


class Node:

    def __init__(self, state, g, parent, data):
        self.state = state
        self.h = state.heuristic(data)
        self.g = g
        self.f = g + self.h
        self.parent = parent
        self.key = str(self.state.key())
        # could store level, but I don't see a point

    def __le__(self, b):
        return self.f < b.f or self.f == b.f and self.h < b.h

    def __gt__(self, b):
        return self.f > b.f or self.f == b.f and self.h > b.h

    def __eq__ (self, b):
        return self.key == b.key

    def __hash__(self):
        return hash(self.key)

    def return_key(self):
        return self.key

    def print_backwards_path(self):
        self.state.print_information()
        if not self.parent:
            return
        self.parent.print_backwards_path()

    def print_path(self, thelist):
        self.collect_path(thelist)
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

class RNode:

    def __init__(self, state, g, parent, data):
        self.state = state
        self.h = state.heuristic(data)
        self.g = g
        self.f = g + self.h
        self.parent = parent
        self.key = str(self.state.key())
        # could store level, but I don't see a point

    def __le__(self, b):
        return self.f > b.f or self.f == b.f and self.h > b.h

    def __gt__(self, b):
        return self.f < b.f or self.f == b.f and self.h < b.h

    def __eq__ (self, b):
        return self.key == b.key

    def __hash__(self):
        return hash(self.key)

    def return_key(self):
        return self.key

    def print_backwards_path(self, data):
        self.state.print_information(data)
        if not self.parent:
            return
        self.parent.print_backwards_path(data)


def convertfromSNode(node, data):
    rNode = RNode(node.state, node.g, node.parent, data)
    return rNode

def convertfromRNode(node, data):
    sNode = Node(node.state, node.g, node.parent, data)
    return sNode

def push(listset, depth, mdepth, node, data):
    listset[depth].push(node)
    listset[depth + mdepth].push(convertfromSNode(node, data))

def popfirst(listset, depth, mdepth):
    node = listset[depth].pop()
    listset[depth + mdepth].remove(node)
    return node

def poplast(listset, depth, mdepth, data):
    node = convertfromRNode(listset[depth + mdepth].pop(), data)
    listset[depth].remove(node)
    return node

def remove(listset, depth, mdepth, node):
    listset[depth].remove(node)
    listset[depth + mdepth].remove(node)

def gen_move_children(current, actBW, waitBW, openlist,
    waitlist, closedlist, dep, mdepth, solution_c, data):
    #print("Depth is " + str(dep))
    genc = 0
    if dep == mdepth-1:
        return genc
    childcollect = current.state.create_children (data)
    #print("Number of children is " + str(len(childcollect)))
    for i in range(len(childcollect)):
        #print(i)
        c = Node (childcollect[i], current.g + 1, current, data)
        inlist = False
        for i in range(mdepth): #altering this has serious effects
            if c in openlist[i]:
                #print("Hello")
                if c.g < openlist[i][c].g:
                    remove (openlist, i, mdepth, c)
                    push (openlist, dep+1, mdepth, c, data)
                inlist = True
                break
            if c in waitlist[i]:
                if c.g < waitlist[i][c].g:
                    remove (waitlist, i, mdepth, c)
                    push (openlist, dep+1, mdepth, c, data)
                inlist = True
            if c.key in closedlist[i]:
                #print("Hi")
                if c.g < closedlist[i][c.key].g:
                    closedlist[i].pop(c.key)
                    push (openlist, dep+1, mdepth, c, data)
                inlist = True
                break
        if not inlist:
            #print("Hello?")
            genc += 1
            push (openlist, dep+1, mdepth, c, data)
        #print(inlist)
        #if len(openlist[dep+1]) + len(closedlist[dep+1])-actBW
        if len(openlist[dep+1]) + len(closedlist[dep+1]) > actBW: #corresponds to 10  #using while here
        #reduces active beam width to acceptable range, but doesn't fix the mismatch
            #print("Hi")
            if not closedlist[dep+1]:
                transfer = poplast(openlist, dep+1, mdepth, data)
                push (waitlist, dep+1, mdepth, transfer, data)
                if len(waitlist[dep+1]) > waitBW:
                    poplast(waitlist, dep+1, mdepth, data)
            else:
                #print("Closed list length is " + str(len(closedlist[dep+1])))
                closedlist[dep+1].popitem()
                #print("Closed list length is now " + str(len(closedlist[dep+1])))
                #end of child generation code
    #print("Gencount this time is " + str(genc))
    #print(len(openlist[dep+1]), actBW)
    #print(len(openlist[dep+1]) + len(closedlist[dep+1]) + len(waitlist[dep+1]))
    return genc

def search_algorithm (filename, startstate, data, bwidth, mdepth, finalwidth):
    openlist = [0 for i in range(mdepth * 2)]
    waitlist = [0 for i in range(mdepth * 2)]
    closedlist = [0 for i in range(mdepth)] #creates the initial lists of structures
    for i in range(mdepth):
        openlist[i] = IHeap([])
        openlist[i + mdepth] = IHeap([])
        waitlist[i] = IHeap([])
        waitlist[i + mdepth] = IHeap([])
        closedlist[i] = OrderedDict()   #correspond to line 3
    solution_c = mdepth #substitute for infinity to avoid an unreasonably high number of digits
    goal = None
    goalcount = 0
    countlist = []
    beamlist = []
    initial = Node(startstate, 0, None, data)
    push (openlist, 0, mdepth, initial, data)
    actBW = 1
    waitBW = bwidth - actBW
    expandcount = 0
    gencount = 0
    while True:
        for dep in range(solution_c):
            #print(dep)
            while openlist[dep]:
                current = popfirst (openlist, dep, mdepth)
                #print(current.h)
                if current.h == 0:
                    if current.f < solution_c:
                        solution_c = current.f
                        goal = current
                        goalcount += 1
                        countlist.append(current.f)
                        beamlist.append(actBW)
                    closedlist[dep][current.key] = current
                    #print(closedlist[dep])
                    continue
                closedlist[dep][current.key] = current
                gencount += gen_move_children(current, actBW, waitBW, openlist,
    waitlist, closedlist, dep, mdepth, solution_c, data)
                if actBW < finalwidth + 1:
                    print(current.key)
                    print("Active beamwidth was " + str(actBW))
                    print("Depth was " + str(dep))
                expandcount += 1
                #print(closedlist[dep])
                #print("Closed list length is " + str(len(closedlist[dep])))
                #print("Active beamwidth is " + str(actBW))
        if waitBW > 0:
            actBW += 1
            waitBW -= 1
            #print(waitBW)
            for dep2 in range(solution_c):
                if waitlist[dep2]:
                    #I cannot see how a duplicate node could get in, so I will not be checking
                    transfer = poplast(waitlist, dep2, mdepth, data)
                    push(openlist, dep2, mdepth, transfer, data)
        else:
            #print("File: " + filename)
            #print("Beamwidth: " + str(bwidth))
            #print("Max Depth: " + str(mdepth))
            if goal:
                #print("Done!\n" + "g: " + str(goal.g) + "\n")
                goal.state.print_information(data)
                #print("Total goal count: " + str(goalcount))
                #print ("Costs were: " + str(countlist))
                #print("Beamwidths were:  " + str(beamlist))
            else:
                #print("Search was unsuccessful")
            #print("Nodes expanded: " + str(expandcount))
            #print("Distinct nodes generated: " + str(gencount) + "\n")
                """
            for i in range(len(openlist)):
                print("For " + str(i))
                for key in openlist[i].dct.keys():
                    print(type(key))
                    """
            
            return
    """
    pathlist = []
    current.print_path_a(pathlist)
    #current.print_backwards_path()
    """



if __name__=='__main__':
    PARSE = argparse.ArgumentParser()
    #creates parser
    PARSE.add_argument("-i", help='input file path (shortened)', type=str)
    PARSE.add_argument("-t", help='type of domain in lowercase', type=str)
    PARSE.add_argument("-w", help='beam width', type=int)
    PARSE.add_argument("-d", help='maximum depth', type=int)
    PARSE.add_argument("-f", help='final printing width', type=int)
    arguments = PARSE.parse_args()
    #parses arguments
    if not arguments.i:
        print("No input file was given.")
    else:
        if not os.path.exists("C:/Users/melis/" + arguments.i):
        #if file cannot be found
            raise ValueError("File could not be found.")
            #raise Value Error (file could not be found)
        else:
            if arguments.t == "blocksworld":
                from blocksworld import read_file
            elif arguments.t == "slidingtiles":
                from slidingtiles import read_file
            data, initstate = read_file("C:/Users/melis/"+ arguments.i)
            print(arguments.i)
            search_algorithm(arguments.i, initstate, data, arguments.w, arguments.d, arguments.f)