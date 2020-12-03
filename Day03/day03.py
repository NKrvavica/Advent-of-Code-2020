# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:08:50 2020

@author: Nino
"""


with open('input.txt', 'r') as f:
    mapp = f.read().split('\n')


def find_trees(mapp, step):
    nr_cols = len(mapp[0])
    x, y = [0, 0]
    tree_counter = 0
    while y < len(mapp)-1:
        y += step[1] # move down
        x = (x + step[0]) % nr_cols # move right
        if mapp[y][x] == '#':
            tree_counter += 1
    return tree_counter


# part 1
step = (3, 1)
how_many_trees = find_trees(mapp, step)
print(f'Solution to part 1. Trees encountered: {how_many_trees}')


# part 2
steps = [(1, 1),
         (5, 1),
         (7, 1),
         (1, 2)]
tree_multiplyer = how_many_trees # start with the solution to part 1
for step in steps:
    how_many_trees = find_trees(mapp, step)
    tree_multiplyer *= how_many_trees
print(f'Solution to part 2. All trees multiplied: {tree_multiplyer}')



