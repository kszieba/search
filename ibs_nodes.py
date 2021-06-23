# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
from red_black_tree import RedBlackTree

class Node:

    def __init__(self, state, g, parent, data):
        self.state = state
        self.g = g
        self.f = g + state.heuristic(data)
        self.parent = parent
        self.key = self.state.key()
        # could store level, but I don't see a point

    def __lt__(self, b):
        return self.f < b.f or (self.f == b.f and self.g > b.g)
    
    def __le__(self, b):
        return self < b or (self.f == b.f and self.g == b.g)

    def __gt__(self, b):
        return self.f > b.f or (self.f == b.f and self.g < b.g)
    
    def __ge___(self, b):
        return self > b or (self.f == b.f and self.g == b.g)

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

    def __init__(self, key, g, f):
        self.g = g
        self.f = f
        self.key = key
        # could store level, but I don't see a point

    def __lt__(self, b):
        return self.f > b.f or (self.f == b.f and self.g < b.g)

    def __gt__(self, b):
        return self.f < b.f or (self.f == b.f and self.g > b.g)
    
    def __le__(self, b):
        return self < b or (self.f == b.f and self.g == b.g)

    def __ge__(self, b):
        return self > b or (self.f == b.f and self.g == b.g)

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


def convertfromSNode(key, g, f):
    rNode = RNode(key, g, f)
    return rNode

def push(listset, depth, mdepth, node):
    if type(listset[depth]) != RedBlackTree:
        listset[depth].push(node)
        listset[depth + mdepth].push(convertfromSNode(node.key, node.g, node.f))
        #except: print(depth, depth + mdepth, file=sys.stderr)
    else:
        listset[depth].insert(node)

def popfirst(listset, depth, mdepth):
    if type(listset[depth]) != RedBlackTree:
        node = listset[depth].pop()
        listset[depth + mdepth].remove(node)
    else:
        node = listset[depth].pop_min()
    return node
        
def poplast(listset, depth, mdepth):
    if type(listset[depth]) != RedBlackTree:
        node = listset[depth].remove(listset[depth + mdepth].pop())
    else:
        node = listset[depth].pop_max()
    return node

def remove(listset, depth, mdepth, node):
    listset[depth].remove(node)
    listset[depth + mdepth].remove(node)

"""
def check_node(listset, depth, mdepth):
    if type(listset[depth]) != RedBlackTree:
        node = listset[depth + mdepth].get_top()
    else:
        node = listset[depth].get_max()
    if node <
"""