# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 11:40:55 2020

@author: Nino
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 09:10:15 2020

@author: Nino
"""

from collections import defaultdict
from itertools import product


def load_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n\n')
    return data


def parse_rules(rules_txt):
    rules = defaultdict()
    for rule in rules_txt.split('\n'):
        # print(rule)
        rule_idx, subrule = rule.split(': ')
        # print(rule_idx, subrule)
        if '"' in subrule:
            subrule = subrule.replace('"','')
        elif '|' in subrule:
            first, second = subrule.split(' | ')
            first_subrule = [nr for nr in first.split(' ')]
            second_subrule = [nr for nr in second.split(' ')]
            subrule = [first_subrule, second_subrule]
        else:
            subrule = [[nr for nr in subrule.split(' ')]]
        rules[rule_idx] = subrule
    return rules


def valid_messages(rules, buffer, rule_idx):
    if rule_idx in buffer: # return if merged
        return buffer[rule_idx]
    rule = rules[rule_idx]
    if isinstance(rule, str): # return if letter
        # print(f'letter: {rule}')
        buffer[rule_idx] = rule
        return rule
    possible_strings = []
    for ors in rule:
        temp = []
        for next_idx in ors:
            temp.append(valid_messages(rules, buffer, next_idx))
        possible_strings.extend(''.join(ch) for ch in product(*temp))
    buffer[rule_idx] = possible_strings
    return possible_strings


# =============================================================================
# Part 1
# =============================================================================
rules_txt, messages_txt = load_input('input.txt')
rules = parse_rules(rules_txt)
valid_mssg = set(valid_messages(rules, {}, '0'))
messages = set([mssg for mssg in messages_txt.split('\n')])
print(f'Solution to part 1: {len(messages.intersection(valid_mssg))}')


# =============================================================================
# Part 2
# =============================================================================
'''
modify rules
rules['8'] = [['42'], ['42', '8']]
rules['11'] = [['42', '31'], ['42', '11', '31']]

NOTE: 0: 8 11
solve 42 and 31, and then figure out what to do next
'''

valid_mssg_42 = set(valid_messages(rules, {}, '42'))
valid_mssg_31 = set(valid_messages(rules, {}, '31'))
block_size = len(next(iter(valid_mssg_42)))

messages = list([mssg for mssg in messages_txt.split('\n')])


'''
valid messages have the format:
[42] * n + [42] * m + [31] * m , where n=1..N, m=1..M
'''

valid_mssgs = 0
for message in messages:
    i = 0
    mssg_format = []
    nr_31, nr_42 = 0, 0
    valid = True
    while i + block_size <= len(message):
        part = message[i:i + block_size]
        if part in valid_mssg_42:
            if 31 in mssg_format: # imaš već 31, ne može 42 ići iza njega!
                valid = False
                break
            else:
                nr_42 += 1
                mssg_format.append(42)
        elif part in valid_mssg_31:
            if mssg_format == []:  # prvi broj mora biti 42, ne može 31!
                valid = False
                break
            else:
                nr_31 += 1
                if nr_31 >= nr_42: # brojeva 31 mora biti manje od 42!
                    valid = False
                    break
                else:
                    mssg_format.append(31)
        else:
            valid = False # ništa od navedeno, reka sam ne može!
            break
        i += block_size
    if valid and mssg_format[-1] == 31:  # zadnji mora biti 31 (barem jedan)
        valid_mssgs += 1
        
print(f'Solution to part 2: {valid_mssgs}')
