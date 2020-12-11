# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 05:37:37 2020

@author: Nino
"""

import numpy as np

def parse_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n')
    return data


# input
layout = parse_input(fname='input.txt')
ROWS, COLS = len(layout), len(layout[0])
num_layout = np.zeros((ROWS, COLS))
for i, row in enumerate(layout):
    for j, seat in enumerate(row):
        if seat == '.':
            num_layout[i, j] = 0
        else:
            num_layout[i, j] = 1


def slice_up(a, idx, limit, step=3):
    lower, upper = max(0, idx - 1), min(limit, idx + 2)
    return a[lower:upper]


def adjecent_seats(occupancy, i, j):
    u, d = max(0, i - 1), min(ROWS, i + 2)
    l, r = max(0, j - 1), min(COLS, j + 2)
    return (occupancy[u:d, l:r] == 9).sum()


def eye_sight(line, pos):
    ctr = 0
    for idx in range(pos+1, len(line)):
        if line[idx] != 0:
            if line[idx] == 9:
                ctr += 1
                break
            else:
                break
    for idx in range(pos-1, -1, -1):
        if line[idx] != 0:
            if line[idx] == 9:
                ctr += 1
                break
            else:
                break
    return ctr


def adjecent_seats2(occupancy, i, j):
    counter = 0

    horizontal = occupancy[i, :]
    counter += eye_sight(horizontal, j)

    vertical = occupancy[:, j]
    counter += eye_sight(vertical, i)

    diagonal = np.diag(occupancy, j-i)
    counter += eye_sight(diagonal, min(i, j))

    diagonal_right = np.diag(np.fliplr(occupancy), (COLS-1-j)-i)
    counter += eye_sight(diagonal_right, min((COLS-1-j), i))

    return counter

    
def simulation(layout, find_seats_func):
    occupancy = layout.copy()
    while True:
        occupancy_new = np.zeros_like(layout)
        for i, row in enumerate(layout):
            for j, seat in enumerate(row):
                if seat == 1:
                    if  (occupancy[i, j]  == 1
                         and find_seats_func(occupancy, i, j) == 0):
                        occupancy_new[i, j] = 9
                    elif (occupancy[i, j]  == 9
                          and find_seats_func(occupancy, i, j) >= 5):
                        occupancy_new[i, j] = 1
                    else:
                        occupancy_new[i, j] = occupancy[i, j]
                else:
                    occupancy_new[i, j] = seat
        if np.array_equal(occupancy, occupancy_new):
            return occupancy_new
        else:
            occupancy = occupancy_new.copy()

# part 1
occupancy = simulation(layout=num_layout, find_seats_func=adjecent_seats)
p1 = (occupancy == 9).sum()


# part 2
occupancy = simulation(layout=num_layout, find_seats_func=adjecent_seats2)
p2 = (occupancy == 9).sum()


print(f'Solution to part 1: {p1}')
print(f'Solution to part 2: {p2}')
