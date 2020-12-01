# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 09:01:42 2020

@author: Nino
"""

import numpy as np
import itertools

report = np.loadtxt(fname = 'input.txt', dtype ='int')

# part one
for a, b, in itertools.combinations(report, 2):
    if a + b == 2020:
        print(f'Solution to part one: {a * b}')

# part two
for a, b, c in itertools.combinations(report, 3):
    if a + b + c == 2020:
        print(f'Solution to part two: {a * b * c}')

# function that does the same as above but for any range of numbers
def do_the_thing(list_of_numbers, sum_value, n):
    for numbers in itertools.combinations(list_of_numbers, n):
        if sum(numbers) == sum_value:
            return print(f'Solution: {np.prod(numbers)}')

do_the_thing(report, 2020, 2)
do_the_thing(report, 2020, 3)
