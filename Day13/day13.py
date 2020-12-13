# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 08:50:08 2020

@author: Nino
"""

from functools import reduce


# earliest = 939
# note = '7,13,x,x,59,x,31,19'
# list_of_buses = note.split(',')


def parse_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n')
    earliest = int(data[0])
    list_of_buses = data[1].split(',')
    return earliest, list_of_buses


def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False


def part1(earliest, list_of_buses):
    best_bus, min_wait = 0, earliest
    buses, lags = [], []
    for i, busID in enumerate(list_of_buses):
        if isint(busID):
            busID = int(busID)
            buses.append(busID)
            lags.append(i)
            depart_in = busID - (earliest % busID)
            print(f'bus ID {busID}, departs in {depart_in}')
            if depart_in <= min_wait:
                min_wait, best_bus = depart_in, busID
    print(f'Best bus: bus ID {best_bus}, departs in {min_wait} min \n')
    return buses, lags, best_bus, min_wait


'''I copied the main function for the chinese remainder theorem:
    https://en.wikipedia.org/wiki/Chinese_remainder_theorem
'''
def chinese_remainder(n, a):
    sums = 0
    prod = reduce(lambda a, b: a*b, n) # product of all elements in the list
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sums += a_i * mul_inv(p, n_i) * p
    return sums % prod
  
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1



# part 1
earliest, list_of_buses = parse_input('input.txt')
buses, lags, best_bus, min_wait = part1(earliest, list_of_buses)
print(f'Solution to part 1: {best_bus*min_wait}\n')

# part 2
remainder = [bus - lag for bus, lag in zip(buses, lags)]
p2 = chinese_remainder(buses, remainder)
print(f'Solution to part 2: {p2} ')
