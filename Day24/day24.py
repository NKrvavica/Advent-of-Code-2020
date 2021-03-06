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


def turn_tiles(parsed_instruc):
    floor = {}
    for instructions in parsed_instruc:
        x, y = 0, 0
        for instruc in instructions:
            x += MOVE[instruc][0]
            y += MOVE[instruc][1]
        if (x, y) in floor:
            floor[(x, y)] = not floor[(x, y)]
        else:
            floor[(x, y)] = True
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
floor = turn_tiles(parsed_instruc)
print(f'Solution to part 1: {sum(floor.values())}')



@njit
def living_art_exhibit(floor, days):
    
    MOVE = {'e': (1, 0),
        'se': (0, 1),
        'sw': (-1, 1),
        'w': (-1, 0),
        'nw': (0, -1),
        'ne': (1, -1)}
    

    def to_check(floor):
        tiles_to_check = set()
        for tile, is_black in floor.items():
            # print(tile, is_black)
            if is_black:
                tiles_to_check.add((tile))
                for _, coord in MOVE.items():
                    neighbour_tile = (coord[0] + tile[0], coord[1] + tile[1])
                    tiles_to_check.add(neighbour_tile)
        return tiles_to_check        


    def sum_adjecent_tiles(floor, i, j):
        counter = 0
        for _, coord in MOVE.items():
            neighbour_tile = (coord[0] + i, coord[1] + j)
            if neighbour_tile in floor:
                if floor[neighbour_tile]: counter += 1
        return counter
    
    for day in range(days):        
        # new day, new floor
        new_floor = {}  
        tiles_to_check = to_check(floor)
        for i, j in tiles_to_check:
            # print(i, j)
            black_tiles = sum_adjecent_tiles(floor, i, j)
            if (i, j) in floor:
                if floor[(i, j)] and 0 < black_tiles <= 2:
                    new_floor[(i, j)] = True
                elif not floor[(i, j)] and black_tiles == 2:
                    new_floor[(i, j)] = True
            else:
                if black_tiles == 2:
                    new_floor[(i, j)] = True 
        floor = new_floor

    return floor



# part 2
days = 3200
floor2 = numba.typed.Dict()
for key, value in floor.items():
    floor2[key] = value
floor = living_art_exhibit(floor2, days)
print(f'Solution to part 2: {sum(floor.values())}')
print(f'Run time: {time() - msStart:.6f} s')


# =============================================================================
# PLOT
# =============================================================================
# def pointy_hex_to_pixel(q, r, size=1):
#     x = size * (math.sqrt(3) * q  +  math.sqrt(3)/2 * r)
#     y = size * (3/2 * r)
#     return np.array([x, y])

# vertical_boundary = np.argwhere(floor)
# down = vertical_boundary[:, 0].min() - 1
# up = vertical_boundary[:, 0].max() + 1

# black_tiles, white_tiles = [], []
# for i, row in enumerate(floor[down:up+1], down):
#     horizontal_boundary = np.argwhere(floor[i-1:i+2])
#     left = horizontal_boundary[:, 1].min() - 1
#     right = horizontal_boundary[:, 1].max() + 1
#     for j, tile in enumerate(row[left:right+1], left):
#         if tile:
#             black_tiles.append(pointy_hex_to_pixel(i, j))
#         else:
#             white_tiles.append(pointy_hex_to_pixel(i, j))

# black_tiles = np.array(black_tiles)
# white_tiles = np.array(white_tiles)

# fig, ax = plt.subplots()
# plt.scatter(white_tiles[:, 0], white_tiles[:, 1], s=30, c='w', edgecolors='k',
#             marker='h', linewidth=0.1)
# plt.scatter(black_tiles[:, 0], black_tiles[:, 1], s=30, c='k', marker='h')
# ax.set_aspect('equal')
