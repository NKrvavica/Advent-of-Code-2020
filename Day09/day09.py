# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 08:23:06 2020

@author: Nino
"""

from itertools import combinations


def parse_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n')
    data = list(map(int, data))
    return data


def find_invalid_number(data, length):
    for i, number in enumerate(data[length:]):
        possible_sums = set()
        preamble = data[i:i+length]
        for two_num in combinations(preamble, 2):
            possible_sums.add(sum(two_num))
        if number not in possible_sums:
            return number


def search(data, invalid_number):
    for i, number in enumerate(data):
        sum_cont = number
        for j, numb in enumerate(data[i+1:], i+1):
            sum_cont += numb
            if sum_cont == invalid_number:
                return data[i:j]
            elif sum_cont > invalid_number:
                break


# input
data = parse_input('input.txt')

# part 1
p1 = find_invalid_number(data, 25)

# part 2
cont = search(data, p1)
p2 = min(cont) + max(cont)


print(f'Solution to part 1: {p1}')
print(f'Solution to part 2: {p2}')
