# -*- coding: utf-8 -*-
# Red Black Tree implementation in Python 2.7
# Author: Algorithm Tutor
# Tutorial URL: https://algorithmtutor.com/Data-Structures/Tree/Red-Black-Trees/

#edited

"""
This red-black tree allows inserting, popping the max, and popping the min. It
is not intended for searching beyond that. It is also capable of retaining
duplicates and returning them when appropriate.
"""

import sys

# data structure that represents a node in the tree
class Node():
    def __init__(self, data):
        self.data = data  # holds the key
        self.parent = None #pointer to the parent
        self.left = None # pointer to left child
        self.right = None #pointer to right child
        self.color = 1 # 1 . Red, 0 . Black


# class RedBlackTree implements the operations in Red Black Tree
class RedBlackTree():
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL
        self.length = 0
        
    def __len__(self):
        return self.length
    
    def __bool__(self):
        if self.length > 0:
            return True
        else:
            return False

    # fix the rb tree modified by the delete operation
    def __fix_delete(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        # case 3.3
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    # case 3.1
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 0 and s.right.color == 0:
                    # case 3.2
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        # case 3.3
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left 

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    # fix the red-black tree
    def  __fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left # uncle
                if u.color == 1:
                    # case 3.1
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # case 3.2.2
                        k = k.parent
                        self.right_rotate(k)
                    # case 3.2.1
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right # uncle

                if u.color == 1:
                    # mirror case 3.1
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent 
                else:
                    if k == k.parent.right:
                        # mirror case 3.2.2
                        k = k.parent
                        self.left_rotate(k)
                    # mirror case 3.2.1
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def __print_helper(self, node, indent, last):
        # print the tree structure on the screen
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.data) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    # find the node with the minimum key
    def pop_min(self):
        node = self.root
        while node.left != self.TNULL:
            node = node.left

        res = node.data
        z = node
        y = node
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.__fix_delete(x)
    
        self.length -=1
        #print("popped min")
        return res

    # find the node with the maximum key
    def pop_max(self):
        node = self.root
        while node.right != self.TNULL:
            node = node.right

        res = node.data
        z = node
        y = node
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.__fix_delete(x)

        #print("popped max")
        self.length -=1        
        return res

    # rotate left at node x
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # rotate right at node x
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # insert the key to the tree in its appropriate position
    # and fix the tree
    def insert(self, key):
        # Ordinary Binary Search Insertion
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1 # new node must be red

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        # y is parent of x
        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node
            
        #print("inserted")
        self.length += 1

        # if new node is a root node, simply return
        if node.parent == None:
            node.color = 0
            return

        # if the grandparent is None, simply return
        if node.parent.parent == None:
            return
        # Fix the tree
        self.__fix_insert(node)

    # print the tree structure on the screen
    def pretty_print(self):
        self.__print_helper(self.root, "", True)

    def is_empty(self):
        return self.root == self.TNULL

if __name__ == "__main__":

#junk class is a class used for testing. It is not intended to hold actual values.

    class junk:
        def __init__(self, h, g, state=0):
            self.f = g+h
            self.h = h
            self.g = g
            self.state = state

        def __repr__(self):
            return "(f="+str(self.f)+",h="+str(self.h)+",g="+str(self.g)+","+str(self.state)+")"

        def __lt__(self, other):
            if self.f < other.f: return True
            elif self.f == other.f and self.h < other.h: return True
            else: return False

        def __le__(self, other):
            return self < other or (self.f == other.f and self.h == other.h)

        def __gt__(self, other):
            if self.f > other.f: return True
            elif self.f == other.f and self.h > other.h: return True
            else: return False

        def __ge__(self, other):
            return self > other or (self.f == other.f and self.h == other.h)

        def __eq__(self, other):
            return self.state == other.state

        def __hash__(self):
            return hash(self.state)

    h = RedBlackTree()
    h.pretty_print()
    print()
    h.insert(junk(0,5,"a"))
    h.pretty_print()
    print()
    j = junk(2,3)
    h.insert(j)
    h.pretty_print()
    print()
    h.insert(junk(3,2,"b"))
    h.pretty_print()
    print()
    k = junk(1,4,"c")
    h.insert(k)
    h.pretty_print()
    print()
    h.insert(junk(2,4,"d"))
    h.pretty_print()
    print()
    h.insert(junk(3,0,"e"))
    h.pretty_print()
    print()
    h.insert(junk(3,0,"f"))
    h.pretty_print()
    print()
    h.insert(junk(3,0,"g"))
    h.pretty_print()
    print()
    h.insert(junk(3,0,"h"))
    h.pretty_print()
    print()
    n = junk(2,2,"c")
    h.insert(n)
    h.pretty_print()
    print()

    print("Mins:")
    while not h.is_empty():
        print(h.pop_min())

    print()


    h = RedBlackTree()
    h.insert(junk(0,5,"a"))
    j = junk(2,3)
    h.insert(j)
    h.insert(junk(3,2,"b"))
    k = junk(1,4,"c")
    h.insert(k)
    h.insert(junk(2,4,"d"))
    h.insert(junk(3,0,"e"))
    h.insert(junk(3,0,"f"))
    h.insert(junk(3,0,"g"))
    h.insert(junk(3,0,"h"))
    n = junk(2,2,"c")
    h.insert(n)

    print("Maxes:")
    while not h.is_empty():
        print(h.pop_max())
        
    """bst = RedBlackTree()
    bst.insert(8)
    bst.insert(18)
    bst.insert(5)
    bst.insert(15)
    bst.insert(17)
    bst.insert(25)
    bst.insert(40)
    bst.insert(80)
    bst.delete_node(25)
    bst.pretty_print()"""