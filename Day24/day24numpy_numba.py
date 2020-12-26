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
import numba

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
days = 1
max_len = days + 2 * max_instruc_len
floor = turn_tiles(parsed_instruc, max_len)
print(f'Solution to part 1: {floor.sum()}')




@njit
def living_art_exhibit(floor, days, max_len):

    def get_boundaries(floor):
        boundary = np.argwhere(floor)
        down = boundary[:, 0].min() - 1
        up = boundary[:, 0].max() + 1
        left = boundary[:, 1].min() - 1
        right = boundary[:, 1].max() + 1
        return down, up, left, right

    def sum_adjecent_tiles(floor, down, up, left, right):
        sum_black = (0 + floor[down-1:up, left:right+1]
                     + floor[down-1:up, left+1:right+2]
                     + floor[down:up+1, left-1:right]
                     + floor[down:up+1, left+1:right+2]
                     + floor[down+1:up+2, left-1:right]
                     + floor[down+1:up+2, left:right+1])
        return sum_black

    for day in range(days):        
        # new day, new floor
        new_floor = np.zeros(shape=(max_len, max_len),
                             dtype=numba.boolean)    
        down, up, left, right = get_boundaries(floor)
        black_tiles = sum_adjecent_tiles(floor, down, up, left, right)
        black_mask1 = floor[down:up+1, left:right+1] & (0 < black_tiles) & (black_tiles <= 2)
        black_mask2 = (~floor[down:up+1, left:right+1]) & (black_tiles==2)
        new_floor[down:up+1, left:right+1] = black_mask1 | black_mask2
        floor = new_floor

    return floor


# part 2
floor = living_art_exhibit(floor, days, max_len)
print(f'Solution to part 2: {floor.sum()}')
print(f'Run time: {time() - msStart:.6f} s')

