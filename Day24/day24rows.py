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
days = 20
max_len = days + 2 * max_instruc_len
floor = turn_tiles(parsed_instruc, max_len)
print(f'Solution to part 1: {floor.sum()}')



boolean = 'bool'
# @njit
def living_art_exhibit(floor, days, max_len):
    
    def vertical_boundaries(floor):
        vertical_boundary = np.argwhere(floor)
        down = vertical_boundary[:, 0].min() - 1
        up = vertical_boundary[:, 0].max() + 1        
        return down, up

    def horizontal_boundaries(floor, i):
        horizontal_boundary = np.argwhere(floor[i-1:i+2])
        left = horizontal_boundary[:, 1].min() - 1
        right = horizontal_boundary[:, 1].max() + 1
        return left, right

    def sum_adjecent_tiles(floor, i, j):
        return (floor[i-1:i+2, j-1:j+2].sum()
                - np.diag(floor[i-1:i+2, j-1:j+2]).sum())

    for day in range(days):        
        # new day, new floor
        new_floor = np.zeros(shape=(max_len, max_len),
                             dtype=boolean)    
        down, up = vertical_boundaries(floor)
        for i, row in enumerate(floor[down:up+1], down):
            left, right = horizontal_boundaries(floor, i)
            for j, tile in enumerate(row[left:right+1], left):
                black_tiles = sum_adjecent_tiles(floor, i, j)
                if tile and 0 < black_tiles <= 2:
                    new_floor[i, j] = True
                elif not tile and black_tiles == 2:
                    new_floor[i, j] = True    

        floor = new_floor

    return floor


# part 2
floor = living_art_exhibit(floor, days, max_len)
print(f'Solution to part 2: {floor.sum()}')
print(f'Run time: {time() - msStart:.6f} s')

# =============================================================================
# PLOT
# =============================================================================
def pointy_hex_to_pixel(q, r, size=1):
    x = size * (math.sqrt(3) * q  +  math.sqrt(3)/2 * r)
    y = size * (3/2 * r)
    return np.array([x, y])

vertical_boundary = np.argwhere(floor)
down = vertical_boundary[:, 0].min() - 1
up = vertical_boundary[:, 0].max() + 1

black_tiles, white_tiles = [], []
for i, row in enumerate(floor[down:up+1], down):
    horizontal_boundary = np.argwhere(floor[i-1:i+2])
    left = horizontal_boundary[:, 1].min() - 1
    right = horizontal_boundary[:, 1].max() + 1
    for j, tile in enumerate(row[left:right+1], left):
        if tile:
            black_tiles.append(pointy_hex_to_pixel(i, j))
        else:
            white_tiles.append(pointy_hex_to_pixel(i, j))

black_tiles = np.array(black_tiles)
white_tiles = np.array(white_tiles)

fig, ax = plt.subplots()
plt.scatter(white_tiles[:, 0], white_tiles[:, 1], s=30, c='w', edgecolors='k',
            marker='h', linewidth=0.1)
plt.scatter(black_tiles[:, 0], black_tiles[:, 1], s=30, c='k', marker='h')
ax.set_aspect('equal')
