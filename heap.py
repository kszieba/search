# -*- coding: utf-8 -*-
"""

"""

def parent(i):
    return int((i-1)/2)

def left(i):
    return 2*i+1

def right(i):
    return 2*i+2

class Heap:
    def __init__(self, lst):
        self.lst = list(lst)
        self.n = len(lst)
        self.dct = {}
        self.__heapify__()
        for i in range(self.n):
            self.dct[self.lst[i]] = i

    def __swap__(self, i, j):
        ki = self.lst[i]
        kj = self.lst[j]

        temp = self.lst[i]
        self.lst[i] = self.lst[j]
        self.lst[j] = temp
        self.dct[ki] = j
        self.dct[kj] = i

    def __moveDown__(self, i):
        while True:
            if left(i) >= self.n:
                return i
            else:
                child = self.lst[left(i)]
                ci = left(i)
                if right(i) < self.n and self.lst[right(i)] < child:
                    child = self.lst[right(i)]
                    ci = right(i)
                if self.lst[i] < child:
                    return i
                else:
                    self.__swap__(ci, i)
                    i = ci
        return i

    def __moveUp__(self, i):
        while True:
            if i == 0:
                return i
            else:
                p = self.lst[parent(i)]
                pi = parent(i)
                if p < self.lst[i]:
                    return i
                else:
                    self.__swap__(pi, i)
                    i = pi
        return i

    def __heapify__(self):
        for i in range(int(self.n/2-1), -1, -1):
            self.__moveDown__(i)

    def __repr__(self):
        return str(self.lst[:self.n])

    def __getitem__(self, v):
        return self.lst[self.dct[v]]

    def __setitem__(self, v, nv):
        self.lst[self.dct[v]] = nv
        tmp = self.dct[v]
        del self.dct[v]
        self.dct[nv] = tmp
        self.__moveUp__(self.dct[nv])
        self.__moveDown__(self.dct[nv])

    def __contains__(self, v):
        return v in self.dct

    def decrease_key(self, val):
        i = self.dct[val]
        self.lst[i] = self.lst[i]
        self.dct[val] = self.__moveUp__(i)

    def push(self, val):
        if(self.n < len(self.lst)):
            self.lst[self.n] = val
        else:
            self.lst.append(val)
        self.n += 1
        self.dct[val] = self.__moveUp__(self.n-1)
        
    def pop(self):
        res = self.lst[0]
        self.__swap__(0, self.n-1)
        self.n = self.n-1
        self.__moveDown__(0)
        del self.dct[res]
        return res

    def is_empty(self):
        return self.n <= 0


if __name__ == "__main__":

    class junk:
        def __init__(self, h, g, state=0):
            self.f = g+h
            self.h = h
            self.g = g
            self.state = state

        def __repr__(self):
            return "("+str(self.f)+","+str(self.h)+","+str(self.g)+","+str(self.state)+")"

        def __lt__(self, other):
            if self.f < other.f: return True
            elif self.f == other.f and self.h < other.h: return True
            else: return False

        def __eq__(self, other):
            return self.state == other.state

        def __hash__(self):
            return hash(self.state)
            
        
    h = heap([])
    print(h)
    h.push(junk(0,5,1))
    print(h)
    j = junk(2,3)
    h.push(j)
    print(h)
    h.push(junk(3,2,2))
    print(h)
    k = junk(1,4,3)
    h.push(k)
    print(h)
    h.push(junk(2,4,4))
    print(h)
    h.push(junk(3,0,5))
    print(h)
    j.g = 1
    j.f = 3
    print(h)
    h.decrease_key(j)
    print(h)
    n = junk(1,2,3)
    h[k] = n
    print(h)

    print("junk with state 1"+["is not in heap", " is in heap"][junk(1,1,1) in h])
    print("junk with state 7"+[" is not in heap", " is in heap"][junk(0,5,7) in h])
    
    h = heap([5,1,4,3,2])
    print(h)
    print(h.pop())
    print(h)
    h.push(0)
    print(h)
    h.push(3.5)
    print(h)
    print(h.pop())
    print(h)
    print("Clearing out heap")
    while(not h.is_empty()):
        print(h.pop())
        print(h)
    print("Done clearing")

    for p in [5,1,4,3,2]:
        h.push(p)
        print(h)
    
    print("Clearing out heap")
    while(not h.is_empty()):
        print(h.pop())
        print(h)
    print("Done clearing")

