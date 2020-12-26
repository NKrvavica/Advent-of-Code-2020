# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 09:38:10 2020

@author: Nino
"""

import re
import math
import matplotlib.pyplot as plt
import numpy as np
from time import time
from numba import njit
from numba import boolean

msStart = time()

def load_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n')
    return data


def parse_input(instructions):
    re_directions = re.compile(r'nw|ne|se|sw|e|w')
    parsed_instruc = [re.findall(re_directions, line) for line in instructions]
    max_instruc_len = max([len(line) for line in instructions])
    return parsed_instruc, max_instruc_len


def turn_tiles(parsed_instruc, max_len):
    floor = np.zeros((max_len, max_len), dtype='bool')    
    for instructions in parsed_instruc:
        # print(instruc)
        x, y = floor.shape[0]//2, floor.shape[1]//2
        for instruc in instructions:
            x += MOVE[instruc][0]
            y += MOVE[instruc][1]
        floor[x, y] = not floor[x, y]
    return floor

MOVE = {'e': (1, 0),
        'se': (0, 1),
        'sw': (-1, 1),
        'w': (-1, 0),
        'nw': (0, -1),
        'ne': (1, -1)}


instructions = load_input('input.txt')
parsed_instruc, max_instruc_len = parse_input(instructions)

# part 1
days = 3200
max_len = days + 2 * max_instruc_len
floor = turn_tiles(parsed_instruc, max_len)
print(f'Solution to part 1: {floor.sum()}')


    
# boolean = 'bool'
@njit
def living_art_exhibit(floor, days, max_len):
    
    MOVE = {'e': (1, 0),
        'se': (0, 1),
        'sw': (-1, 1),
        'w': (-1, 0),
        'nw': (0, -1),
        'ne': (1, -1)}

    def to_check(floor):
        vertical_boundary = np.argwhere(floor)
        tiles_to_check = set()
        for tile in vertical_boundary:
            tiles_to_check.add((tile[0], tile[1]))
            for side, coord in MOVE.items():
                new_tile = (coord[0] + tile[0], coord[1] + tile[1])
                tiles_to_check.add(new_tile)
        return tiles_to_check        
                
    def sum_adjecent_tiles(floor, i, j):
        return (floor[i-1:i+2, j-1:j+2].sum()
                - np.diag(floor[i-1:i+2, j-1:j+2]).sum())

    for day in range(days):        
        # new day, new floor
        new_floor = np.zeros(shape=(max_len, max_len),
                             dtype=boolean)    
        tiles_to_check = to_check(floor)
        for i, j in tiles_to_check:
            black_tiles = sum_adjecent_tiles(floor, i, j)
            if floor[i, j] and 0 < black_tiles <= 2:
                new_floor[i, j] = True
            elif not floor[i, j] and black_tiles == 2:
                new_floor[i, j] = True    

        floor = new_floor

    return floor, tiles_to_check


# part 2
floor, tiles_to_check = living_art_exhibit(floor, days, max_len)
print(f'Solution to part 2: {floor.sum()}')
print(f'Run time: {time() - msStart:.6f} s')

