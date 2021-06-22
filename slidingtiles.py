# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

import os.path
import copy

class State:

    def __init__(self, locationlist, zeroindex, ntype=None):
        self._locationlist = locationlist
        self._ntype = ntype
        self._zeroindex = zeroindex
        
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
    

    def get_simple_new_tuple (self, orig, break1, break2):
        return orig[:break1] + (orig[break2],) \
            + (orig[break1],) + orig[break2 + 1:]
            
    def get_complex_new_tuple (self, orig, break1, break2):
        return orig[:break1] + (orig[break2],) + orig[break1+1:break2] \
            + (orig[break1],) + orig[break2 + 1:]

        
    def create_children (self, dimens):
        childlist = []
        zeroindex = self._zeroindex
        #print(zeroindex)
        if zeroindex > dimens-1 and self._ntype != "d":
            uc_locationlist = self.get_complex_new_tuple(self._locationlist, zeroindex - dimens, zeroindex)
            #print(uc_locationlist)
            uc_zeroindex = zeroindex - dimens
            uc = State(uc_locationlist, uc_zeroindex, "u")
            childlist.append(uc)
            #print("Hello???")
        if (zeroindex + 1) % dimens and self._ntype != "l":
            rc_locationlist = self.get_simple_new_tuple(self._locationlist, zeroindex, zeroindex + 1)
            #print(rc_locationlist)
            rc_zeroindex = zeroindex + 1
            rc = State(rc_locationlist, rc_zeroindex, "r")
            childlist.append(rc)
            #print("Hello?")
        if zeroindex % dimens and self._ntype != "r":
            lc_locationlist = self.get_simple_new_tuple(self._locationlist, zeroindex - 1, zeroindex)
            #print(lc_locationlist)
            lc_zeroindex = zeroindex - 1
            lc = State(lc_locationlist, lc_zeroindex, "l")
            childlist.append(lc)
            #print("Hello??")
        if zeroindex < (dimens-1) * dimens and self._ntype != "u":
            dc_locationlist = self.get_complex_new_tuple(self._locationlist, zeroindex, zeroindex + dimens)
            #print(dc_locationlist)
            dc_zeroindex = zeroindex + dimens
            dc = State(dc_locationlist, dc_zeroindex, "d")
            childlist.append(dc)
            #print("Hello????")
        return childlist
    
    def find_value (self, index, goalnumber, dimens):
        if goalnumber == 0:
            return 0
        dcount = abs(goalnumber // dimens - index // dimens)
        ncount = abs(goalnumber % dimens - index % dimens)
        return dcount + ncount

    def heuristic (self, dimens):
        total = 0
        for i in range(len (self._locationlist)):
            total += self.find_value(i, self._locationlist[i], dimens)
            #print(self.find_value(i, self._locationlist[i]))
        return total
    
    def key(self):
        return str(self._locationlist)

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
    locationslist = [0 for i in range(dimens * dimens)]
    for i in range(dimens * dimens):
        locationslist[int(locations[i])] = i
        if i == 0:
            zeroindex = int(locations[i])
    locationlist = tuple(locationslist)
    state = State(locationlist, zeroindex)
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