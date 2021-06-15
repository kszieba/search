# -*- coding: utf-8 -*-
"""
This heap does not work with duplicates and can be expected to react badly to 
them. However, it works well for handling two types of nodes used to form
pairs.
"""

def parent(i):
    return int((i-1)/2)

def left(i):
    return 2*i+1

def right(i):
    return 2*i+2

class Heap_with_keys:
    def __init__(self, alist):
        self.alist = [alist]
        self.n = len(alist)
        #length of list within heap
        self.dct = {}
        #defines dictionary for heap (with dictionary, key is item and other is place)
        self.__heapify__()
        for i in range(self.n):
            self.dct[self.alist[i].key] = i
            
    def __bool__(self):
        if self.n > 0:
            return True
        else:
            return False
            
    def __len__(self):
        return self.n

    def __swap__(self, i, j):
        ki = self.alist[i].key
        kj = self.alist[j].key
        temp = self.alist[i]
        #temporarily set variable to the ith element
        self.alist[i] = self.alist[j]
        #change ith element to match jth one
        self.alist[j] = temp
        #change jth element to match temp
        self.dct[ki] = j
        self.dct[kj] = i
        #swap values within dictionary
        
    def __moveDown__(self, i):
        while True:
            if left(i) >= self.n:
            #if 2i + 1 is greater than the length of the list
                return i
            else:
                child = self.alist[left(i)]
                #item with index 2i +1 is child
                ci = left(i)
                if right(i) < self.n and self.alist[right(i)] < child:
                    child = self.alist[right(i)]
                    ci = right(i)
                if self.alist[i] < child:
                    return i
                else:
                    self.__swap__(ci, i)
                    #swap two elements
                    i = ci
        return i
        #return new index

    def __moveUp__(self, i):
        while True:
            if i == 0:
            #if i is already 0
                return i
            else:
                p = self.alist[parent(i)]
                pi = parent(i)
                if p <= self.alist[i]:
                    if p == self.alist[i] and p.h > self.alist[i].h:
                        self.__swap__(pi, i)
                        i = pi
                    return i
                else:
                    self.__swap__(pi, i)
                    i = pi
        return i

    def __heapify__(self):
        for i in range(int(self.n/2-1), -1, -1):
            self.__moveDown__(i)
            
    def __getitem__(self, v):
        return self.alist[self.dct[v.key]]
    
    def __contains__(self, v):
        return v.key in self.dct
    
    def __setitem__(self, v, nv):
        self.alist[self.dct[v.key]] = nv
        tmp = self.dct[v.key]
        del self.dct[v.key]
        self.dct[nv.key] = tmp
        self.__moveUp__(self.dct[nv.key])
        self.__moveDown__(self.dct[nv.key])

    def push(self, node):
        if(self.n < len(self.alist)):
        #if list is longer than official length
            self.alist[self.n] = node
        else:
            self.alist.append(node)
        self.n += 1
        self.dct[node.key] = self.__moveUp__(self.n-1)
        
    def pop(self):
        res = self.alist[0]
        #set res to first item in list
        self.__swap__(0, self.n-1)
        self.n = self.n-1
        self.__moveDown__(0)
        del self.dct[res.key]
        #delets res from dictionary
        return res
    
    def remove(self, val):
        i = self.dct[val.key]
        res = self.alist[i]
        self.__swap__(i, self.n-1)
        self.n = self.n-1
        self.__moveDown__(i)
        del self.dct[res.key]
        return res