# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

import os.path
import copy

class State:

    def __init__(self, dimens, locations):
    #initializes class, taking two parameters including self
        self._locationlist = [0 for i in range(dimens * dimens)]
        for i in range(dimens * dimens):
            self._locationlist[int(locations[i])] = i
        self._ntype = None
        
    def print_information(self, dimens):
        print(str(dimens) + " x " + str(dimens) + "\n")
        for i in range(1, dimens+1):
            piece = (self._locationlist[dimens * (i-1):dimens * i])
            for number in piece:
                if dimens > 3:
                    if number > 9:
                        print(str(number) + " ", end = "")
                    elif number == 0:
                        print("__ ", end = "")
                    else:
                        print(" " + str(number) + " ", end = "")
                else:
                    if number != 0:
                        print(str(number) + " ", end = "")
                    else:
                        print("_ ", end = "")
            print("\n", end = "")
        print ("\nh: " + str(self.heuristic(dimens))+ "\n")
        
    def print_goal(self, dimens):
        print(str(dimens) + " x " + str(dimens) + "\n")
        for i in range(1, dimens+1):
            piece = (self._locationlist[dimens * (i-1):dimens * i])
            for number in piece:
                if dimens > 3:
                    if number > 9:
                        print(str(number) + " ", end = "")
                    elif number == 0:
                        print("__ ", end = "")
                    else:
                        print(" " + str(number) + " ", end = "")
                else:
                    if number != 0:
                        print(str(number) + " ", end = "")
                    else:
                        print("_ ", end = "")
            print("\n", end = "")
        
    def create_children (self, dimens):
        childlist = []
        zeroindex = self._locationlist.index(0)
        if zeroindex > dimens-1 and self._ntype != "d":
            uc = copy.deepcopy(self)
            uc._locationlist[zeroindex] = uc._locationlist[zeroindex - dimens]
            uc._locationlist[zeroindex - dimens] = 0
            uc._ntype = "u"
            childlist.append(uc)
            #print("Hello???")
        if (zeroindex + 1) % dimens and self._ntype != "l":
            rc = copy.deepcopy(self)
            rc._locationlist[zeroindex] = rc._locationlist[zeroindex+1]
            rc._locationlist[zeroindex+1] = 0
            rc._ntype = "r"
            childlist.append(rc)
            #print("Hello?")
        if zeroindex % dimens and self._ntype != "r":
            lc = copy.deepcopy(self)
            lc._locationlist[zeroindex] = lc._locationlist[zeroindex-1]
            lc._locationlist[zeroindex-1] = 0
            lc._ntype = "l"
            childlist.append(lc)
            #print("Hello??")
        if zeroindex < (dimens-1) * dimens and self._ntype != "u":
            dc = copy.deepcopy(self)
            dc._locationlist[zeroindex] = dc._locationlist[zeroindex + dimens]
            dc._locationlist[zeroindex + dimens] = 0
            dc._ntype = "d"
            childlist.append(dc)
            #print("Hello????")
        return childlist
    
    def find_value (self, index, goalnumber, dimens):
        
        dcount = abs(goalnumber // dimens - index // dimens)
        ncount = abs(goalnumber % dimens - index % dimens)
        if goalnumber == 0:
            return 0
        return dcount + ncount

    def heuristic (self, dimens):
        total = 0
        for i in range(len (self._locationlist)):
            total += self.find_value(i, self._locationlist[i], dimens)
            #print(self.find_value(i, self._locationlist[i]))
        return total
    
    def key(self):
        return self._locationlist

def read_file(inputfile):
    readingfile = open (inputfile, "r")
    count = 1
    locations = []
    for line in readingfile:
        if count == 1:
            dimens = int(line[0])
        elif 2 < count < (dimens * dimens + 3):
            locations.append(line.strip())
        elif count > (dimens * dimens + 3):
            break
        count = count + 1
    state = State(dimens, locations)
    return dimens, state
        
if __name__=='__main__':        
#if called from the terminal
    filename = "10042"
    if os.path.exists("C:/Users/melis/8_puzzles/8_puzzles/"+filename):
        dimens, state = read_file("C:/Users/melis/8_puzzles/8_puzzles/"+filename)
        #dimens, locations = read_file("C:/Users/melis/8_puzzles/8_puzzles/"+filename)
        #state = State (dimens, locations)
        state._locationlist = [1, 2, 3, 4, 0, 6, 7, 8, 5]
        state._0location = 4
        state.print_information(dimens)
        print("Children's Information\n")
        childrenlist = state.create_children(dimens)
        for child in childrenlist:
            child.print_information(dimens)
            
        print(state.find_value(5, 6, dimens))