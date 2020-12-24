# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 11:57:56 2020

@author: Nino
"""

'''Optimizirat ću, trenutno koristim map<int, set<pair<list<int>, list<int>>>>
i imam neke bolje ideje
'''

from collections import deque
from time import time


# =============================================================================
# INPUT
# =============================================================================
cup_str = '784235916'
# cup_str = '389125467' # example


# =============================================================================
# PART 1
# =============================================================================
cup = deque(map(int, list(cup_str)))
SIZE = len(cup)
MIN = min(cup)
MAX = max(cup)


def take_three(cup, ci):
    cup.rotate(SIZE - 4 - ci)
    three = deque()
    for _ in range(3):
        three.appendleft(cup.pop())
    return three
    

def add_three(cup, three_cups, di):
    cup.rotate(SIZE - 4 - di)
    for nr in three_cups:
        cup.append(nr)
    return cup


def solve_part1(cup, ci=0, rounds=100):
    for _ in range(rounds):
        current = cup[ci]
        three_cups = take_three(cup, ci)
        destination = current - 1
        if destination < MIN:
            destination= MAX
        while destination in three_cups:
            destination -= 1
            if destination < MIN:
                destination= MAX
        di = cup.index(destination)
        cup = add_three(cup, three_cups, di)
        ci = (cup.index(current) + 1) % SIZE
    return cup

msStart = time()
cup = solve_part1(cup, 0, 100)
one_idx = cup.index(1)
cup.rotate(-one_idx)
p1 = ''.join(map(str, list(cup)[1:]))
print(f'Solution to part 1: {p1}')
print(f'Run time: {time() - msStart:.6f} s')


# =============================================================================
# PART 2
# =============================================================================
cup = list(map(int, list(cup_str)))
add_cup = list(range(10, 1_000_000 + 1))
cup += add_cup
SIZE = len(cup)
MIN = min(cup)
MAX = max(cup)

def linked_list(cup):
    # generate linked list via dictionary
    cup_linked = {}
    for i in range(len(cup)-1):
        cup_linked[cup[i]] = cup[i+1]
    cup_linked[cup[len(cup)-1]] = cup[0] # conncet last element to the first (cycle)
    return cup_linked


def solve_part2(cup_linked, ci=0, rounds=10_000_000):
    current = cup[ci]
    for br in range(10000000 + 1):
        if br % 100000 == 0:
            print(f'{br/10_000_000*100}%')
        
        # take three cups
        one = cup_linked[current]
        two = cup_linked[one]
        three = cup_linked[two]
        three_cups = [one, two, three]
        cup_linked[current] = cup_linked[three]
        
        # find destination
        destination = current - 1
        if destination < MIN:
            destination = MAX
        while destination in three_cups:
            destination -= 1
            if destination < MIN:
                destination = MAX
        
        # add three cups
        cup_linked[three] = cup_linked[destination]
        cup_linked[destination] = one
        
        current = cup_linked[current]
        
    return cup_linked


msStart = time()
cup_linked = linked_list(cup)
cup_linked = solve_part2(cup_linked, 0, 10_000_000)
first_cup = cup_linked[1]
second_cup = cup_linked[first_cup]
p2 = first_cup * second_cup
print(f'Solution to part 2: {p2}')
print(f'Run time: {time() - msStart:.6f} s')
