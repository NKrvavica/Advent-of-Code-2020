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


def slice_up(a, idx, limit, step=3):
    lower, upper = max(0, idx - 1), min(limit, idx + 2)
    return a[lower:upper]


def adjecent_seats(occupancy, i, j):
    occupied_seats = 0
    for row in (slice_up(occupancy, i, ROWS)):
        for seat in (slice_up(row, j, COLS)):
            if seat == '#':
                occupied_seats += 1
    return occupied_seats



def adjecent_seats2(occupancy, i, j):
    occupied_seats = 0
    for n in range(j+1, COLS):
        # print(i, n, occupancy[i][n])
        if occupancy[i][n] != '.':
            if occupancy[i][n] == '#':
                occupied_seats += 1
                break
            else:
                break
    for n in range(j-1, -1, -1):   
        # print(i, n, occupancy[i][n])
        if occupancy[i][n] != '.':
            if occupancy[i][n] == '#':
                occupied_seats += 1
                break
            else:
                break
    for m in range(i+1, ROWS):   
        # print(m, j, occupancy[m][j])
        if occupancy[m][j] != '.':
            if occupancy[m][j] == '#':
                occupied_seats += 1
                break
            else:
                break
    for m in range(i-1, -1, -1):   
        # print(m, j, occupancy[m][j])
        if occupancy[m][j] != '.':
            if occupancy[m][j] == '#':
                occupied_seats += 1
                break
            else:
                break

    n, m = i+1, j+1
    while 0 <= n < ROWS and 0 <= m < COLS:
        # print(n, m, occupancy[n][m])
        if occupancy[n][m] != '.':
            if occupancy[n][m] == '#':
                occupied_seats += 1
                break
            else:
                break
        n += 1
        m += 1

    n, m = i-1, j+1
    while 0 <= n < ROWS and 0 <= m < COLS:
        # print(n, m, occupancy[n][m])
        if occupancy[n][m] != '.':
            if occupancy[n][m] == '#':
                occupied_seats += 1
                break
            else:
                break
        n -= 1
        m += 1

    n, m = i-1, j-1
    while 0 <= n < ROWS and 0 <= m < COLS:
        # print(n, m, occupancy[n][m])
        if occupancy[n][m] != '.':
            if occupancy[n][m] == '#':
                occupied_seats += 1
                break
            else:
                break
        n -= 1
        m -= 1

    n, m = i+1, j-1
    while 0 <= n < ROWS and 0 <= m < COLS:
        # print(n, m, occupancy[n][m])
        if occupancy[n][m] != '.':
            if occupancy[n][m] == '#':
                occupied_seats += 1
                break
            else:
                break
        n += 1
        m -= 1

    return occupied_seats
    

def simulation(layout, find_seats_func):
    occupancy = layout
    while True:
        occupancy_new = []
        for i, row in enumerate(layout):
            row_occupancy = ''
            for j, seat in enumerate(row):
                if seat == 'L':
                    if  (occupancy[i][j] == 'L'
                         and find_seats_func(occupancy, i, j) == 0):
                        row_occupancy += '#'
                    elif (occupancy[i][j] == '#'
                          and find_seats_func(occupancy, i, j) >= 5):
                        row_occupancy += 'L'
                    else:
                        row_occupancy += occupancy[i][j]
                else:
                    row_occupancy += seat
            occupancy_new.append(row_occupancy)
        if occupancy == occupancy_new:
            return occupancy
        else:
            occupancy = occupancy_new


# part 1
occupancy = simulation(layout, adjecent_seats)
p1 = 0
for row in occupancy:
    p1 += row.count('#')


# part 2
occupancy = simulation(layout, adjecent_seats2)
p2 = 0
for row in occupancy:
    p2 += row.count('#')


print(f'Solution to part 1: {p1}')
print(f'Solution to part 2: {p2}')
