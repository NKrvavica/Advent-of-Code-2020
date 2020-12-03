# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:08:50 2020

@author: Nino
"""


def find_trees(mapp, step):
    x, y = step
    tree_counter = 0
    while y < map_height:
        if mapp[y][x] == '#':
            tree_counter += 1
        y += step[1] # move down
        x = (x + step[0]) % map_width # move right
    return tree_counter


# read the input
with open('input.txt', 'r') as f:
    mapp = f.read().split('\n')

# get the map size    
map_height, map_width = len(mapp), len(mapp[0])

# part 1
step = (3, 1)
trees_in_part_one = find_trees(mapp, step)
print(f'Solution to part 1. Trees encountered: {trees_in_part_one}')

# part 2
steps = [(1, 1), (5, 1), (7, 1), (1, 2)]
tree_multiplyer = trees_in_part_one # start with the solution to part 1
for step in steps:
    how_many_trees = find_trees(mapp, step)
    tree_multiplyer *= how_many_trees
print(f'Solution to part 2. All trees multiplied: {tree_multiplyer}')



