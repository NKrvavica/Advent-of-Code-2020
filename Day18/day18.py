# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 06:59:44 2020

@author: Nino
"""

import re
import operator
import copy
from pyparsing import nestedExpr


# =============================================================================
# FUNCTIONS
# =============================================================================

def load_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n')
    return data


def parse_math(expr):
    'get list of numbers and operators of an expression'
    operators = set('+*')
    ops, nums, digits = [], [], []
    for ch in expr:  
        if ch in operators:  
            nums.append(''.join(digits))
            ops.append(ch)
            digits = []
        else:
            digits.append(ch)
    nums.append(''.join(digits))
    return nums, ops


def advanced_math(zadatak):
    '''evaluate a single expression inside brackets using advanced operation
    precedence'''
    nums, ops = parse_math(zadatak)   
    value = None
    for op in ADV_OP_ORDER:                   # Loop over operators in order of presedence
        while op in ops:        # Operator with this precedence level exists
            idx, oo = next((i, o) for i, o in enumerate(ops) if o in op) # Next operator with this precedence         
            ops.pop(idx)                        # remove this operator from the operator list
            values = list(map(int, nums[idx: idx+2]))
            value = OPERATION[oo](*values)
            nums[idx:idx+2] = [value]           

    return nums[0]



def simple_math(zadatak):
    '''evaluate a single expression inside brackets without any operation
    precedence'''
    nums, ops = parse_math(zadatak)   
    value = int(nums[0])
    for num, op in zip(nums[1:], ops):
        value = OPERATION[op](value, int(num))
    return value


def do_the_math(nested_exp, eval_math):
    '''recursive function for navigating through complex expressions
    given as a list, each element in a list is either a part of expression
    or a list of lists of lists... of single expressions'''
    for i, part_of_expr in enumerate(nested_exp):
        if isinstance(part_of_expr, list): 
            if len(part_of_expr) == 1:
                nested_exp[i] = str(eval_math(part_of_expr[0]))
            else:
                nested_exp[i] = do_the_math(part_of_expr, eval_math)  
    nested_exp = str(eval_math(''.join(nested_exp)))
    return nested_exp


# =============================================================================
# MAIN
# =============================================================================

OPERATION = {'*': operator.mul, '+': operator.add}
ADV_OP_ORDER = ('+','*')  # presedence order of operators  

homework = load_input('input.txt')

suma1, suma2 = 0, 0
for expression in homework:
    
    # parse input
    expression = '(' + expression.replace(' ','') + ')'
    nested_exp = nestedExpr('(',')').parseString(expression).asList()
    
    # part 1
    math_expression = copy.deepcopy(nested_exp[0])
    s1 = do_the_math(math_expression, simple_math)
    suma1 += int(s1)
    
    # part 2
    math_expression = nested_exp[0]
    s2 = do_the_math(math_expression, advanced_math)
    suma2 += int(s2)


print(f'Solution to part 1: {suma1}')
print(f'Solution to part 2: {suma2}')
