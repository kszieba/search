# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 14:35:55 2021

@author: melis
"""

from ibs_katrina import search_algorithm

import slidingtiles

import blocksworld


for i in range(1, 101, 20):
    data, initstate = slidingtiles.read_file("C:/Users/melis/korf100/" + str(i))
    filename = "korf100/" + str(i)
    for beam in range(20, 61, 20):
        for depth in range(70, 101, 10):
            search_algorithm(filename, initstate, data, beam, depth)

for name in ("4puzzle1", "9puzzle2", "12puzzle1", "15puzzle2", "18puzzle1"):
    data, initstate = blocksworld.read_file("C:/Users/melis/blocksworld_puzzles/blocks" + name +".txt")
    filename = "Blocks_world_puzzles/" + name
    for beam in range(20, 61, 20):
        for depth in range(70, 101, 10):
            search_algorithm(filename, initstate, data, beam, depth)
for i in range(5, 30, 5):
    data, initstate = slidingtiles.read_file("C:/Users/melis/8_puzzles/" + str(i) +"42")
    filename = "8_puzzles/" + str(i) + "42"
    for beam in range(20, 60, 20):
        for depth in range(70, 100, 10):
            search_algorithm(filename, initstate, data, beam, depth)