# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 08:41:26 2020

@author: Nino
"""

import numpy as np

# examples
# boarding_passes = ['FBFBBFFRLR', 'BFFFBBFRRR', 'FFFBBBFRRR', 'BBFFBBFRLL']

with open('input.txt') as f:
    boarding_passes = f.read().split('\n')


def decode(codes, letter, max_number):
    low, high = 0, max_number-1
    for code in codes:
        if code == letter: 
            high = (low + high) // 2
        else:
            low = (low + high) // 2 + 1
    return low

    
def decode_boarding_passes(boarding_passes):
    seatIDs = []
    for boarding_pass in boarding_passes:
        row = decode(boarding_pass[:7], 'F', 128)
        column = decode(boarding_pass[7:], 'L', 8)
        seatID = row*8 + column
        seatIDs.append(seatID)
    return seatIDs
    

# part 1
seatIDs = decode_boarding_passes(boarding_passes)
maxID = max(seatIDs)
print(f'Solution to part 1. Solution is {maxID}')


# part 2
seatIDs.sort()
location_of_my_seat = np.where(np.diff(seatIDs) == 2)[0]
my_seatID = seatIDs[int(location_of_my_seat)] + 1
print(f'Solution to part 2. Solution is {my_seatID}')
