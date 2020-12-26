# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 09:38:10 2020

@author: Nino
"""

import re
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
    floor = numba.typed.Dict()
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
days = 100
floor = living_art_exhibit(floor, days)
print(f'Solution to part 2: {sum(floor.values())}')
print(f'Run time: {time() - msStart:.6f} s')

