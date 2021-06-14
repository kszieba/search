# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 13:43:12 2021

"""
class Treenode:
    
    def __init__ (self, parent, content):
        self.content = content
        self.parent = parent
        self.lchild = None
        self.rchild = None
        self.color = "red"
    

class red_black_tree:
    
    def __init__(self):
        self.root = Treenode(None, None, None)
        self.root.color = "black"
        self.length = 0
        self.left = None
        self.right = None
        
    def __len__(self):
        return self.length
    
    def fi


