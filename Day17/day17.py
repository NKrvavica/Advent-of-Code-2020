# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 15:01:45 2020

@author: PC-KRVAVICA
"""

import numpy as np
from time import time


pocket = '''....#...
.#..###.
.#.#.###
.#....#.
...#.#.#
#.......
##....#.
.##..#.#'''

state = []
for s in pocket.split('\n'):
    state.append(list(s.replace('.', '0').replace('#', '1')))

msStart = int(time() * 1000)

init_state = np.array([state], dtype=np.int32)
for n in range(6):
    x, y, z = np.array(np.shape(init_state)) + 2
    new_state = np.zeros((x, y, z))
    old_state = np.zeros((x, y, z))
    old_state[1:-1, 1:-1, 1:-1] = init_state

    for i,j,k in np.ndindex(x,y , z):
        suma = np.sum(old_state[max(0, i-1): min(i+2, x),
                                max(0, j-1): min(j+2, y),
                                max(0, k-1): min(k+2, z)])
        if old_state[i,j,k] == 0 and suma == 3:
            new_state[i,j,k] = 1
        elif old_state[i,j,k] == 1 and suma-1 in range(2, 4):
            new_state[i,j,k] = 1
        else:
            new_state[i,j,k] = 0
    init_state=new_state

print(f'Solution to part 2: {np.sum(init_state)}')
print(f'Run time: {int(time() * 1000) - msStart} ms')

msStart = int(time() * 1000)
init_state = np.array([[state]], dtype=np.int32)
for n in range(6):
    x, y, z, w = np.array(np.shape(init_state)) + 2
    new_state = np.zeros((x, y, z, w))
    old_state = np.zeros((x, y, z, w))
    old_state[1:-1, 1:-1, 1:-1, 1:-1] = init_state

    for i,j,k,l in np.ndindex(x, y, z, w):
        suma = np.sum(old_state[max(0, i-1): min(i+2, x),
                                max(0, j-1): min(j+2, y),
                                max(0, k-1): min(k+2, z),
                                max(0, l-1): min(l+2, w)])
        # print(i,j,k, suma)
        if old_state[i,j,k,l] == 0 and suma == 3:
            new_state[i,j,k,l] = 1
        elif old_state[i,j,k,l] == 1 and suma-1 in range(2, 4):
            new_state[i,j,k,l] = 1
        else:
            new_state[i,j,k,l] = 0
    init_state=new_state

print(f'Solution to part 2: {np.sum(np.sum(init_state))}')
print(f'Run time: {int(time() * 1000) - msStart} ms')
