# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:20:15 2020

@author: Nino
"""

import re
from itertools import product


# =============================================================================
# FUNCTIONS
# =============================================================================

def load_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n')
    return data


def parse_input(data):
    masks, memory = [], []
    mask_nr = -1
    for d in data:
        inst, value = d.split(' = ')
        if inst == 'mask':
            mask_nr += 1
            masks.append(value)
        else:
            pos = re.findall(r'\d+', inst)[0]
            memory.append((int(pos), int(value), mask_nr))
    return masks, memory


def apply_mask(value, mask_i, ver):
    bin_value = '{0:036b}'.format(value)
    masked_value = []
    for v, m in zip(bin_value, masks[mask_i]):
        if m == 'X':
            if ver==1:  masked_value.append(v)
            else:       masked_value.append('X')
        elif m == '1':
            if ver==1:  masked_value.append(m)
            else:       masked_value.append(m)
        elif m == '0':
            if ver==1:  masked_value.append(m)
            else:       masked_value.append(v)
    return ''.join(masked_value)



def find_positions_of_char_in_string(string, char):
    char_positions = []
    for i, c in enumerate(string):
        if c == char:
            char_positions.append(i)
    return char_positions
    # return [i for i, c in enumerate(string) if c == char]


def replace_char(s, ch, idx):
    if idx < 0:  # add it to the beginning
        return ch + s
    elif idx > len(s):  # add it to the end
        return s + ch
    else:  # add inbetween
        return s[:idx] + ch + s[idx + 1:]    
    

# =============================================================================
# MAIN
# =============================================================================

# laod and parse data
data = load_input('input.txt')
masks, memory = parse_input(data)


# part 1
program = {}
for adress, value, mask_i in memory:
    masked_value = apply_mask(value, mask_i, ver=1)
    program[adress] = int(masked_value, 2)

p1 = sum(program.values())
print(f'Solution to part 1: {p1}\n')


# part 2
program = {}
for adress, value, mask_i in memory:
    masked_adress = apply_mask(adress, mask_i, ver=2)
    x_positions = find_positions_of_char_in_string(masked_adress, 'X') 
    for sequence_of_01 in product('01', repeat=len(x_positions)):
        new_adress = masked_adress
        for ch, xpos in zip(sequence_of_01, x_positions):
            new_adress = replace_char(new_adress, ch, xpos)
        program[int(new_adress, 2)] = value

p2 = sum(program.values())
print(f'Solution to part 2: {p2}\n')
