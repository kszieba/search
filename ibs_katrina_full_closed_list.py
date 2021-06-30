# -*- coding: utf-8 -*-
"""
Incremental Beam Search Algorithm
This version assumes cost is constant and does not explore deeper levels than
the one where the current best solution was found.
Created on Tue Jun  8 13:47:52 2021
"""
import os.path
import argparse
import sys

from heap_with_keys import Heap_with_keys

from red_black_tree import RedBlackTree

from ibs_nodes import Node, push, popfirst, poplast, remove

"""
from guppy import hpy
h = hpy()
print(h.heap())
"""

    
class Results:
    
    def __init__(self):
        self.expandcount = 0
        self.gencount = 0
        self.pruneddup = 0
        self.reexpansions = 0
        self.openlist_len = 1
        self.waitlist_len = 0
        self.closedlist_len = 0
        self.max_openlist = 1
        self.max_waitlist = 0 
        self.max_closedlist = 0


def gen_move_children(current, actBW, waitBW, openlist,
    waitlist, closedlist, dep, mdepth, solution_c, data, results):
    #print("Depth is " + str(dep))
    if dep == solution_c - 1:
        return
    childcollect = current.state.create_children (data)
    #print("Number of children is " + str(len(childcollect)))
    ndep = dep + 1
    for i in range(len(childcollect)):
        #print(i)
        c = Node (childcollect[i], current.g + 1, current, data)
        results.gencount += 1
        inlist = False
        if c.f >= solution_c: #very useful
            continue
        for i in range(solution_c): #altering this has serious effects
            if c in openlist[i]:
                if c.g < openlist[i][c].g:
                    remove (openlist, i, mdepth, c)
                    push (openlist, ndep, mdepth, c)
                else:
                    results.pruneddup += 1
                inlist = True
                break
            if c.key in closedlist[i]:
                #print("Hi")
                if c.g < closedlist[i][c.key].g:
                    closedlist[i].pop(c.key)
                    push (openlist, ndep, mdepth, c)
                    results.closedlist_len -= 1
                    results.openlist_len += 1
                    results.reexpansions += 1
                    if results.openlist_len > results.max_openlist:
                        results.max_openlist = results.openlist_len
                else:
                    results.pruneddup += 1
                inlist = True
                break
        if not inlist:
            #print("Hello?")
            push (openlist, ndep, mdepth, c)
            results.openlist_len += 1
            if results.openlist_len > results.max_openlist:
                results.max_openlist = results.openlist_len
        #print(inlist)
        #if len(openlist[dep+1]) + len(closedlist[dep+1])-actBW
        if len(openlist[ndep]) > actBW: #corresponds to 10
            transfer = poplast(openlist, ndep, mdepth)
            push (waitlist, ndep, mdepth, transfer)
            results.openlist_len -= 1
            results.waitlist_len += 1
            if results.waitlist_len > results.max_waitlist:
                results.max_waitlist = results.waitlist_len
            if len(waitlist[ndep]) > waitBW:
                poplast(waitlist, ndep, mdepth)
                results.waitlist_len -= 1
                #print("Closed list length is now " + str(len(closedlist[dep+1])))
                #end of child generation code
    #print("Gencount this time is " + str(genc))
    #print(len(openlist[dep+1]), actBW)
    #print(len(openlist[dep+1]) + len(closedlist[dep+1]) + len(waitlist[dep+1]))
    return

def search_algorithm (filename, startstate, data, bwidth, mdepth, call_type="standard"):
    openlist = [0 for i in range(mdepth * 2)]
    waitlist = [0 for i in range(mdepth)]
    closedlist = [0 for i in range(mdepth)] #creates the initial lists of structures
    for i in range(mdepth):
        openlist[i] = Heap_with_keys([])
        openlist[i + mdepth] = Heap_with_keys([])
        waitlist[i] = RedBlackTree()
        closedlist[i] = {}   #correspond to line 3
    solution_c = mdepth #substitute for infinity to avoid an unreasonably high number of digits
    goal = None
    goalcount = 0
    countlist = []
    beamlist = []
    initial = Node(startstate, 0, None, data)
    push (openlist, 0, mdepth, initial)
    actBW = 1
    waitBW = bwidth - actBW
    results = Results()
    while True:
        for dep in range(solution_c):
            #print(dep)
            while openlist[dep]:
                current = popfirst (openlist, dep, mdepth)
                results.openlist_len -= 1
                if results.openlist_len > results.max_openlist:
                    results.max_openlist = results.openlist_len
                if current.f >= solution_c:
                    continue
                if (current.f - current.g) == 0:
                    if current.f < solution_c:
                        solution_c = current.f
                        goal = current
                        print(dep)
                        goalcount += 1
                        countlist.append(current.f)
                        beamlist.append(actBW)
                    closedlist[dep][current.key] = current
                    results.closedlist_len += 1
                    if results.closedlist_len > results.max_closedlist:
                        results.max_closedlist = results.closedlist_len
                    #print(closedlist[dep])
                    continue
                closedlist[dep][current.key] = current
                results.closedlist_len += 1
                gen_move_children(current, actBW, waitBW, openlist,
    waitlist, closedlist, dep, mdepth, solution_c, data, results)
                results.expandcount += 1
                #print(closedlist[dep])
                #print("Closed list length is " + str(len(closedlist[dep])))
                #print("Active beamwidth is " + str(actBW))
        if waitBW > 0:
            actBW += 1
            waitBW -= 1
            #print(waitBW)
            for dep2 in range(solution_c):
                #print("Hello")
                #waitlist[dep2].pretty_print()
                #print(waitlist[dep2].length)
                if waitlist[dep2]:
                    transfer = popfirst(waitlist, dep2, mdepth)
                    results.waitlist_len -= 1
                    inlist = False
                    for i in range(solution_c): #altering this has serious effects
                        if transfer in openlist[i]:
                            #print("Hello")
                            if transfer.g < openlist[i][transfer].g:
                                remove (openlist, i, mdepth, transfer)
                                push (openlist, dep2, mdepth, transfer)
                            else:
                                results.pruneddup += 1
                            inlist = True
                            break
                        if transfer.key in closedlist[i]:
                            #print("Hi")
                            if transfer.g < closedlist[i][transfer.key].g:
                                closedlist[i].pop(transfer.key)
                                push (openlist, dep2, mdepth, transfer)
                                results.closedlist_len -= 1
                                results.openlist_len += 1
                                if results.openlist_len > results.max_openlist:
                                    results.max_openlist = results.openlist_len
                            else:
                                results.pruneddup += 1
                            inlist = True
                            break
                    if not inlist:
                        push(openlist, dep2, mdepth, transfer)
                        results.openlist_len += 1
                        if results.openlist_len > results.max_openlist:
                            results.max_openlist = results.openlist_len
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
            print("Nodes expanded: " + str(results.expandcount))
            print("Distinct nodes generated: " + str(results.gencount))
            print("Pruned duplicates: " + str(results.pruneddup))
            print("Re-expansions: " + str(results.reexpansions))
            print("Max length of open list: " + str(results.max_openlist))
            print("Max length of wait list: " + str(results.max_waitlist))
            print("Max length of closed list: " + str(results.max_closedlist)  + "\n")
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
        filename = "24puzzles/0"
        domain = "sliding_tiles"
        width = 30
        depth = 660
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