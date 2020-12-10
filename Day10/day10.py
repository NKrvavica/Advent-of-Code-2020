# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 09:51:40 2020

@author: Nino
"""

import numpy as np


def parse_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n')
    data = list(map(int, data))
    return data


def find_differences(adapters):
    outlet, device = [0], [adapters[-1] + 3]
    chain = outlet + adapters + device
    chain_diff = np.diff(chain)
    unique, counts = np.unique(chain_diff, return_counts=True)
    return unique, counts, chain_diff


def compute_permutations(chain_diff):
    nr_ones, permutations = 0, 1
    for i, diff in enumerate(chain_diff):
        if diff == 3:
            permutations *= TRIBONACCI[nr_ones]
            nr_ones = 0
        elif diff == 1:
            nr_ones += 1
    return int(permutations)


# input
adapters = parse_input('input.txt')
adapters.sort()

# part 1
unique, counts, chain_diff = find_differences(adapters)
p1 = counts[0] * counts[1]
print(f'Solution to part 1: {p1}')

# part 2
TRIBONACCI = [1, 1, 2, 4, 7, 13, 24, 44]
p2 = compute_permutations(chain_diff)
print(f'Solution to part 2: {p2}')


# alternative part 2
from collections import Counter
adapters.sort(reverse=True)
chain = adapters + [0]
ways = Counter([adapters[0] + 3])
for ch in chain:
    ways[ch] = ways[ch+3] + ways[ch+2] + ways[ch+1]
p2 = ways[0]
print(f'Solution to part 2 (alternative way): {p2}')
