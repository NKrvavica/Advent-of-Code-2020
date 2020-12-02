# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 08:21:21 2020

@author: Nino
"""

fname = 'input.txt'

with open(fname) as f:
    lines = f.read().splitlines()


def parse_input(line):
    policy, password = line.split(': ')
    numbers, letter = policy.split(' ')
    low, high = map(int, numbers.split('-'))
    return low, high, letter, password


# part 1
counter = 0
for line in lines:
    low, high, letter, password = parse_input(line)
    if low <= password.count(letter) <= high:
        counter += 1

print(f'First part. Number of valid passwords:{counter}')

# part 2
counter = 0
for line in lines:
    first, second, letter, password = parse_input(line)
    if (password[first-1] == letter) ^ (password[second-1] == letter):
        counter += 1

print(f'Second part. Number of valid passwords:{counter}')
