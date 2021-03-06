# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:19:05 2020

@author: Nino
"""

import pandas as pd

# load data
program = pd.read_csv('input.txt', header=None, sep=' ',
                      names=['op', 'arg'])
program_len = len(program)

# run the program
def run_program(program, program_len):
    idx, accumulator = 0, 0
    program['visited']= False

    while True:  
        op, arg, visited = program.loc[idx]

        if visited:
            return program, accumulator, idx
        else:
            program.loc[idx, 'visited'] = True

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
            return program, accumulator, idx
    
    
# part 1
program, accumulator, idx = run_program(program, program_len)
print(f'Solution to part 1: {accumulator} \n')


# part 2
def attempt_brute_forces_changes(program):
    program_len = len(program)
    for i, row in program.iterrows():
        op, arg, visited = row

        if op == 'nop':
            program_copy = program.copy()
            program_copy.loc[i, 'op'] = 'jmp'
            print(f'attempt changing line {i}, from nop to jmp')
        elif op == 'jmp':
            program_copy = program.copy()
            program_copy.loc[i, 'op'] = 'nop'
            print(f'attempt changing line {i}, from jmp to nop,')
        else:
            continue

        program_copy, accumulator, idx = run_program(program_copy, program_len)
        # print(f'program terminated at line {idx}')

        if idx >= program_len:
            return accumulator


accumulator = attempt_brute_forces_changes(program)
print(f'Solution to part 2: {accumulator}')
