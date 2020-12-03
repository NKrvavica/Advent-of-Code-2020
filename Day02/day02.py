# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 08:21:21 2020

@author: Nino
"""

fname = 'input.txt'

with open(fname) as f:
    lines = f.readlines()


def parse_input(line):
    policy, password = line.split(': ')
    numbers, letter = policy.split(' ')
    low, high = map(int, numbers.split('-'))
    return low, high, letter, password


counter_p1, counter_p2 = 0, 0
for line in lines:
    first, second, letter, password = parse_input(line)
    if first <= password.count(letter) <= second:
        counter_p1 += 1
    if (password[first-1] == letter) ^ (password[second-1] == letter):
        counter_p2 += 1

print(f'First part. Number of valid passwords: {counter_p1}')
print(f'Second part. Number of valid passwords: {counter_p2}')


# NOTE!
# alternative option for parsing input line
# import re
# words = re.compile(r'\w+')
# low, high, letter, password = re.findall(words, line)
# low, high = int(low), int(high)
