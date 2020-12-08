# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:19:05 2020

@author: Nino
"""

import pandas as pd

# load data
with open('./input.txt', 'r') as f:
    program = f.read().split('\n')
    
program_len = len(program)

# run the program
def run_program(program, program_len):
    idx, accumulator = 0, 0
    visited = set()

    while True:  
        op, arg = program[idx].split(' ')
        arg = int(arg)

        if idx in visited:
            return accumulator, idx
        else:
            visited.add(idx)

        if op == 'nop':
            idx += 1 
        elif op == 'acc':
            accumulator += arg
            idx += 1
        else:  # op == 'jmp'
            idx += arg

        if idx >= program_len: # this is needed for part 2
            print('Warning! Attempting to run the instruction below the last',
                  'instruction in the file')
            return accumulator, idx
    
    
# part 1
accumulator, idx = run_program(program, program_len)
print(f'Solution to part 1: {accumulator} \n')


# part 2
def attempt_brute_forces_changes(program):
    program_len = len(program)
    for i, row in enumerate(program):

        if row[:3] == 'nop':
            program_copy = program.copy()
            program_copy[i] = 'jmp' + row[3:]
            # print(f'attempt changing line {i}, from nop to jmp')
        elif row[:3] == 'jmp':
            program_copy = program.copy()
            program_copy[i] = 'nop' + row[3:]
            # print(f'attempt changing line {i}, from jmp to nop,')
        else:
            continue

        accumulator, idx = run_program(program_copy, program_len)
        # print(f'program terminated at line {idx}')

        if idx >= program_len:
            return accumulator


accumulator = attempt_brute_forces_changes(program)
print(f'Solution to part 2: {accumulator}')
