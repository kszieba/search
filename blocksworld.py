# -*- coding: utf-8 -*-
"""
Created on Mon May 31 15:47:53 2021

@author: melis
"""

import os.path
import copy

filename = "Puzzle2.txt"

class State:

    def __init__(self, volume, upblocks, downblocks, goal=[0, 1, 0, 3]):
        self._upblocks = upblocks
        #print(self._upblocks)
        #print("Yes?")
        self._dblocks = downblocks
        #if self._upblocks != transform(self._dblocks):
            #print("Alert!")
            #print(self._upblocks, self._dblocks)
            #raise ValueError
        self._goal = goal
        self._topscount = self._calculate_tops(volume)
        
    def _calculate_tops(self, volume):
        self._topspoint = [0 for i in range(volume)]
        topscount = 0
        for i in range(volume):
            if self._upblocks[i] == None:
                self._topspoint[topscount] = i
                topscount += 1
        self._topspoint = self._topspoint[:topscount]
        #print("Topspoint: ", str(self._topspoint))
        return topscount
    
    def _calculate_bottoms(self, volume):
        bpoint = [0 for i in range(volume)]
        #print(self._dblocks)
        bcount = -1
        for i in range(volume):
            if len(self._dblocks)!=volume:
                print("Hello")
                print(volume)
                print(self._dblocks)
            if self._dblocks[i] == None:
                bcount += 1
                bpoint[bcount] = i
        bpoint = bpoint[:bcount +1]
        #print(self._bpoint)
        return bpoint

    def print_information(self, volume):
        b2list = []
        blist = self._calculate_bottoms(volume)
        keeplist = [blist, b2list]
        unfinished = True
        for i in range(len(blist)):
            b2list.append(self._upblocks[blist[i]])
            #print (self._upblocks[blist[i]])
            #print("Hi?")
        pastlist = b2list
        while unfinished:
            newlist = []
            unfound = True
            for i in range(len(pastlist)):
                if pastlist[i] != None:
                    newlist.append(self._upblocks[pastlist[i]])
                    unfound = False
                else:
                    newlist.append(None)
            keeplist.append(newlist)
            pastlist = newlist
            if unfound:
                unfinished = False            
        for alist in keeplist:
            if volume < 10:
                for i in range(len(alist)):
                    if alist[i] == None:
                        alist[i] = " "
                    else:
                        alist[i] = str(int(alist[i])+1)
            else:
                for i in range(len(alist)):
                    if alist[i] == None:
                        alist[i] = "  "
                    else:
                        if len(str(alist[i]+1)) == 2:
                            alist[i] = str(int(alist[i])+1)
                            #print(alist[i])
                        else:
                            alist[i] = str(int(alist[i])+1) + " "
                            #print(alist[i])
        for i in range(len(keeplist)-1, -1, -1):
            print("|" + "| |".join(keeplist[i]) + "|")
        print ("\n", end="")
        print("h: " + str(self.heuristic(volume)))
        
    def print_goal(self, volume):
        b2list = []
        blist = self._calculate_bottoms(volume)
        keeplist = [blist, b2list]
        unfinished = True
        for i in range(len(blist)):
            b2list.append(self._upblocks[blist[i]])
            #print (self._upblocks[blist[i]])
            #print("Hi?")
        pastlist = b2list
        while unfinished:
            newlist = []
            unfound = True
            for i in range(len(pastlist)):
                if pastlist[i] != None:
                    newlist.append(self._upblocks[pastlist[i]])
                    unfound = False
                else:
                    newlist.append(None)
            keeplist.append(newlist)
            pastlist = newlist
            if unfound:
                unfinished = False            
        for alist in keeplist:
            if volume < 10:
                for i in range(len(alist)):
                    if alist[i] == None:
                        alist[i] = " "
                    else:
                        alist[i] = str(int(alist[i])+1)
            else:
                for i in range(len(alist)):
                    if alist[i] == None:
                        alist[i] = "  "
                    else:
                        if len(str(alist[i]+1)) == 2:
                            alist[i] = str(int(alist[i])+1)
                            #print(alist[i])
                        else:
                            alist[i] = str(int(alist[i])+1) + " "
                            #print(alist[i])
        for i in range(len(keeplist)-1, -1, -1):
            print("|" + "| |".join(keeplist[i]) + "|")
        print ("\n")
    
    def heuristic (self, volume):
        #if self._upblocks != transform(self._dblocks):
            #print("Alert!")
            #print(self._upblocks, self._dblocks)
            #raise ValueError
        total = 0
        for i in range(volume):
            if self._dblocks[i] == None:
                current = i
                while current != None:
                    #print (self._dblocks, self._goal)
                    #print(current)
                    if self._dblocks[current] != self._goal[current]:               
                        while self._upblocks[current] != None:
                            total += 1
                            current = self._upblocks[current]
                        total += 1
                        break
                    current = self._upblocks[current]
        return total
        
    def create_children (self, volume):
        #print(self._topscount)
        childlist = [0 for i in range(self._topscount * (self._topscount))]
        childnumber = 0
        #print("Topspoint: ", str(self._topspoint))
        for i in range(self._topscount):
            for j in range(self._topscount):
            #loop for regular generation of children
                #print("j: ", str(j))
                if i != j:
                #if not trying to place a block atop itself
                    #print("Hopefully...")
                    new = copy.deepcopy(self)
                    new._topspoint[j] = self._topspoint[i]
                    #block i replaces block j in topspoint
                    new._upblocks[self._topspoint[j]] = self._topspoint[i]
                    #i block is now above j block
                    new._dblocks[self._topspoint[i]] = self._topspoint[j]
                    # j block is now below i block
                    if self._dblocks[self._topspoint[i]] != None:
                    #if there is a block below the one being moved
                        new._topspoint[i] = self._dblocks[self._topspoint[i]]
                        #that block replaces block i in topspoint
                        new._upblocks[self._dblocks[self._topspoint[i]]] = None
                        #that block has no block above it
                    else:
                    #if block was the last of the stack
                        new._topspoint.remove(self._topspoint[i])
                        new._topscount -= 1
                    #print("1")
                    #new.print_information()
                    #if new._upblocks != transform(new._dblocks):
                        #print("Alert One!")
                        #print(self._upblocks, self._dblocks)
                        #print(new._upblocks, new._dblocks)
                        #raise ValueError
                    childlist[childnumber] = new
                    childnumber += 1
            if self._dblocks[self._topspoint[i]] != None:
                new = copy.deepcopy(self)
                #create copy for move to table
                if self._dblocks[self._topspoint[i]] != None:
                #if there is a block below i block
                    new._topspoint[i] = self._dblocks[self._topspoint[i]]
                    new._upblocks[self._dblocks[self._topspoint[i]]] = None
                    new._dblocks[self._topspoint[i]] = None
                    new._topspoint.append(self._topspoint[i])
                    #print(new._topspoint)
                    new._topscount += 1
                else:
                    new._topspoint.pop(i)
                #print("2")
                #new.print_information()
                #if new._upblocks != transform(new._dblocks):
                        #print("Alert Two!")
                        #print(self._upblocks, self._dblocks)
                        #print(new._upblocks, new._dblocks)
                        #raise ValueError
                childlist[childnumber] = new
                childnumber += 1
                #print(childlist)
        #print(childlist)
        return childlist[:childnumber]
    
    def key(self):
        return str(self._upblocks)

def read_file(inputfile):
    readingfile = open (inputfile, "r")
    count = -2
    for line in readingfile:
        if count == -2:
            volume = int(line)
            #print(volume)
            blocks = [0 for i in range(volume)]
            goals = [0 for i in range(volume)]
        elif -1 < count < (volume):
            blocks[count] = int(line.strip())
            #print(line)
        elif count > (volume):
            goals[count-volume-1] = int(line.strip())
        count = count + 1
    readingfile.close()
    #print(goals)
    #print(blocks)
    downblocks = [None for i in range(volume)]
    upblocks = [None for i in range(volume)]
    revised_goals = convert_to_d(goals, volume)
    for i in range(volume):
        if blocks[i] == 0:
            #print(i)
            downblocks[i] = None
        else:
            downblocks[i] = blocks[i]-1
            upblocks[blocks[i]-1]= i
    #print(downblocks)
    #print(upblocks)
    return volume, State(volume, upblocks, downblocks, revised_goals)

def convert_to_u(downlist, volume):
    upblocks = [None for i in range(volume)]
    for i in range(volume):
        if downlist[i] != 0:
            upblocks[downlist[i]-1]= i
    return upblocks

def convert_to_d(downlist, volume):
    downblocks = [None for i in range(volume)]
    for i in range(volume):
        if downlist[i] == 0:
            downblocks[i] = None
        else:
            downblocks[i] = downlist[i]-1
    #print(downblocks)
    return downblocks

def transform(blocklist):
    newlist = [None for i in range(len(blocklist))]
    for i in range(len(blocklist)):
        if blocklist[i] != None:
            newlist[blocklist[i]] = i
    return newlist
        
if __name__=='__main__':        
#if called from the terminal
    if not os.path.exists("C:/Users/melis/blocksworld_puzzles/"+filename):
        print("Is your filename correct?")
    else: 
        volume, state = read_file("C:/Users/melis/blocksworld_puzzles/"+filename)
        #rint(goals)
        print(volume)
        state2 = State (4, [None, None, None, None], [None, None, None, None])
        state3 = State (4, convert_to_u([0, 1, 2, 3], 4), convert_to_d([0, 1, 2, 3], 4))
        #print(convert_to_u([2, 3, 4, 0], 4))
        testingstate = state2
        testingstate.print_information(4)
        print("Children's Information\n")
        childrenlist = testingstate.create_children(4)
        for child in childrenlist:
            if type(child)==int:
                print("Unexpected int")
            else:
                child.print_information(4)
        newlist = childrenlist[0].create_children(4)
        #print("Hello")
        for child in newlist:
            print(child._upblocks, child._dblocks, child._topspoint)
            if type(child)==int:
                print("Unexpected int")
            else:
                child.print_information(4)