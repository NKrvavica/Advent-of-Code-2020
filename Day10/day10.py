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
    outlet, device = [0], [max(adapters) + 3]
    chain = outlet + adapters + device
    chain_diff = np.diff(chain)
    unique, counts = np.unique(chain_diff, return_counts=True)
    return unique, counts, chain_diff


def compute_permutations(chain_diff):
    '''
    number of consequtive 1s between two 3s are related to the number
    of permutations as:
    (n-1) * n / 2 + 1,
    where n is the number of consecutive 1s, and 1s and 3s are the differences
    between numbers in the list.
    (this took 3 pieces of paper, and one hour to figure out...)'

    '''
    nr_ones, permutations = 0, 1
    for diff in chain_diff:
        if diff == 3:
            permutations *= (nr_ones - 1) * nr_ones / 2 + 1
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
p2 = compute_permutations(chain_diff)
print(f'Solution to part 2: {p2}')
