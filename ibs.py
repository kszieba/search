# -*- coding: utf-8 -*-
"""
Incremental Beam Search Algorithm

This version is closely matched to the orginal algorithm.

Created on Tue Jun  8 13:47:52 2021

"""

import sys

import os.path

import argparse

from collections import OrderedDict

from heap_with_keys import Heap_with_keys

from red_black_tree import RedBlackTree

from ibs_nodes import Node, push, popfirst, poplast, remove

"""
from guppy import hpy
h = hpy()
print(h.heap())
"""


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
        genc += 1
        inlist = False
        for i in range(mdepth): #altering this has serious effects
            if c in openlist[i]:
                #print("Hello")
                if c.g < openlist[i][c].g:
                    remove (openlist, i, mdepth, c)
                    push (openlist, dep+1, mdepth, c, data)
                inlist = True
                break
            """
            if c in waitlist[i]:
                if c.g < waitlist[i][c].g:
                    remove (waitlist, i, mdepth, c)
                    push (openlist, dep+1, mdepth, c, data)
                inlist = True
            """
            if c.key in closedlist[i]:
                #print("Hi")
                if c.g < closedlist[i][c.key].g:
                    closedlist[i].pop(c.key)
                    push (openlist, dep+1, mdepth, c, data)
                inlist = True
                break
        if not inlist:
            #print("Hello?")
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
                closedlist[dep+1].popitem(last=False)
                #print("Closed list length is now " + str(len(closedlist[dep+1])))
                #end of child generation code
    #print("Gencount this time is " + str(genc))
    #print(len(openlist[dep+1]), actBW)
    #print(len(openlist[dep+1]) + len(closedlist[dep+1]) + len(waitlist[dep+1]))
    return genc

def search_algorithm (filename, startstate, data, bwidth, mdepth, call_type="standard"):
    openlist = [0 for i in range(mdepth * 2)]
    waitlist = [0 for i in range(mdepth)]
    closedlist = [0 for i in range(mdepth)] #creates the initial lists of structures
    for i in range(mdepth):
        openlist[i] = Heap_with_keys([])
        openlist[i + mdepth] = Heap_with_keys([])
        waitlist[i] = RedBlackTree()
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
        for dep in range(mdepth):
            #print(dep)
            while openlist[dep]:
                current = popfirst (openlist, dep, mdepth)
                if (current.f - current.g) == 0:
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
                expandcount += 1
                #print(closedlist[dep])
                #print("Closed list length is " + str(len(closedlist[dep])))
                #print("Active beamwidth is " + str(actBW))
        if waitBW > 0:
            actBW += 1
            waitBW -= 1
            #print(waitBW)
            for dep2 in range(mdepth):
                #print("Hello")
                #waitlist[dep2].pretty_print()
                #print(waitlist[dep2].length)
                if waitlist[dep2]:
                    transfer = popfirst(waitlist, dep2, mdepth)
                    inlist = False
                    for i in range(mdepth): #altering this has serious effects
                        if transfer in openlist[i]:
                            #print("Hello")
                            if transfer.g < openlist[i][transfer].g:
                                remove (openlist, i, mdepth, transfer)
                                push (openlist, dep2, mdepth, transfer, data)
                            inlist = True
                            break
                        """
                        if c in waitlist[i]:
                            if c.g < waitlist[i][c].g:
                                remove (waitlist, i, mdepth, c)
                                push (openlist, dep+1, mdepth, c, data)
                            inlist = True
                        """
                        if transfer.key in closedlist[i]:
                            #print("Hi")
                            if transfer.g < closedlist[i][transfer.key].g:
                                closedlist[i].pop(transfer.key)
                                #print("insert depth is " + str(dep+1))
                                push (openlist, dep2, mdepth, transfer, data)
                            inlist = True
                            break
                    if not inlist:
                        push(openlist, dep2, mdepth, transfer, data)
        else:
            print("File: " + filename)
            print("Beamwidth: " + str(bwidth))
            print("Max Depth: " + str(mdepth))
            if goal:
                print("Done!\n" + "g: " + str(goal.g) + "\n")
                print("Total goal count: " + str(goalcount))
                print ("Costs were: " + str(countlist))
                print("Beamwidths were:  " + str(beamlist))
                if call_type == "pictoral":
                    print("\n")
                    goal.state.print_goal(data)
            else:
                print("Search was unsuccessful\n\n")
                print("Total goal count: " + str(goalcount))
                print ("Costs were: " + str(countlist))
                print("Beamwidths were:  " + str(beamlist))
            print("Nodes expanded: " + str(expandcount))
            print("Distinct nodes generated: " + str(gencount) + "\n")
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
    PARSE.add_argument("-d", help='domain name in lowercase', type=str)
    PARSE.add_argument("-w", help='beam width', type=int)
    PARSE.add_argument("-b", help='maximum depth', type=int)
    PARSE.add_argument("-c", help='call type', type=str, required=False)
    arguments = PARSE.parse_args()
    #parses arguments
    if not arguments.i:
        filename = "korf100/12"
        domain = "sliding_tiles"
        width = 60
        depth = 50
    else:
        filename = arguments.i
        if not os.path.exists("C:/Users/melis/" + arguments.i):
            raise ValueError("File could not be found.")      
        domain = arguments.d
        width = arguments.w
        depth = arguments.b
    if domain == "blocksworld":
        from blocksworld import read_file
    elif domain == "sliding_tiles":
        from slidingtiles import read_file
    data, initstate = read_file("C:/Users/melis/"+ filename)
    if arguments.c:
        search_algorithm(filename, initstate, data, width, depth, arguments.c)
    else:
        search_algorithm(filename, initstate, data, width, depth)