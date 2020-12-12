# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 08:29:15 2020

@author: Nino
"""

# =============================================================================
# FUNCTIONS
# =============================================================================

def parse_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n')
    instructions = []
    for d in data:
        instructions.append((d[0], int(d[1:])))
    return instructions


def move(x, y, inst, value):
    x += DIRS[inst][0] * value
    y += DIRS[inst][1] * value
    return x, y


def move_ship(x, y, xway, yway, value):
    x += xway * value
    y += yway * value
    return x, y


def turn(xway, yway, inst, value):
    sign = TURNS[inst]
    for _ in range(value // 90):
        xway, yway = sign * yway, -sign * xway
    return xway, yway


def navigate(x, y, xway, yway, dir_idx, instructions, part=1):
    for inst, value in instructions:
        if inst in DIRS:
            if part==1:     x, y = move(x, y, inst, value)
            else:           xway, yway = move(xway, yway, inst, value)
        elif inst in TURNS:
            if part==1:     dir_idx = (dir_idx + TURNS[inst] * value // 90) % 4
            else:           xway, yway = turn(xway, yway, inst, value)
        elif inst == 'F':
            if part==1:     x, y = move(x, y, [*DIRS][dir_idx], value)
            else:           x, y = move_ship(x, y, xway, yway, value)
    return (abs(x) + abs(y))


# =============================================================================
# Main part
# =============================================================================

# load input
instructions = parse_input('input.txt')

# definitions
DIRS = {'E':(1, 0), 'S':(0, -1), 'W':(-1, 0), 'N':(0, 1)}
TURNS = {'R': 1, 'L': -1}

# part 1
x, y = 0, 0
dir_idx = 0
p1  = navigate(x, y, None, None, dir_idx, instructions, part=1)

# part 2
x, y = 0, 0
xway, yway = 10, 1
p2 = navigate(x, y, xway, yway, None, instructions, part=2)


print(f'Solution to part 1: {p1}')
print(f'Solution to part 2: {p2}')
