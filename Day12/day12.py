# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 08:29:15 2020

@author: Nino
"""

import math
import numpy as np

def parse_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n')
    instructions = []
    for d in data:
        instructions.append((d[0], int(d[1:])))
    return instructions


# =============================================================================
# PART 1 FUNCTIONS
# =============================================================================


def move(x, y, inst, value):
    x += MOVES[inst][0] * value
    y += MOVES[inst][1] * value
    return x, y


def navigate(x, y, dir_idx, instructions):
    for inst, value in instructions:
        if inst in DIRS:
            x, y = move(x, y, inst, value)
        elif inst in TURNS:
            dir_idx = (dir_idx + TURNS[inst] * value // 90) % 4
        elif inst == 'F':
            direction = DIRS[dir_idx]
            x, y = move(x, y, direction, value)
    return abs(x) + abs(y)


# =============================================================================
# PART 2 FUNCTIONS
# =============================================================================


def move_waypoint(xway, yway, inst, value):
    xway += MOVES[inst][0] * value
    yway += MOVES[inst][1] * value
    return xway, yway


def move_ship(x, y, xway, yway, value):
    x += xway * value
    y += yway * value
    return x, y


def cart2pol(i, j):
    rho = math.sqrt(i**2 + j**2)
    phi = math.atan2(j, i)
    return(rho, phi)


def pol2cart(rho, phi):
    i = int(round(rho * math.cos(phi)))
    j = int(round(rho * math.sin(phi)))
    return(i, j)


def rotate(xway, yway, inst, value):
    rho, phi = cart2pol(xway, yway)
    phi += -TURNS[inst] * math.radians(value)
    return pol2cart(rho, phi)


def navigate2(x, y, xway, yway, instructions):
    for inst, value in instructions:
        if inst in DIRS:
            xway, yway = move_waypoint(xway, yway, inst, value)
        elif inst in TURNS:
            xway, yway = rotate(xway, yway, inst, value)
        elif inst == 'F':
            x, y = move_ship(x, y, xway, yway, value)
    return (abs(x) + abs(y))


# =============================================================================
# Main part
# =============================================================================

# load input
instructions = parse_input('input.txt')

#definitions
DIRS = ['E', 'S', 'W', 'N']
MOVES = {'E':(1, 0), 'S':(0, -1), 'W':(-1, 0), 'N':(0, 1)}
TURNS = {'R':1, 'L':-1}
ROT_MAT = np.array([[-1, 0], [0, 1]])

# part 1
x, y = 0, 0
dir_idx = 0
p1  = navigate(x, y, dir_idx, instructions)

# part 2
x, y = 0, 0
xway, yway = 10, 1
p2 = navigate2(x, y, xway, yway, instructions)


print(f'Solution to part 1: {p1}')
print(f'Solution to part 2: {p2}')
