# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 09:30:05 2020

@author: Nino
"""

import string


with open('input.txt') as f:
    declaration_form = f.read().split('\n\n')


total_yeses, total_all_yeses = 0, 0
for groups_answers in declaration_form:

    '''part 1: count the number of questions that were answered yes'''
    group_answer = groups_answers.replace('\n', '')
    total_yeses += len(set(group_answer))

    '''part 2: count the number of questions that were answered yes by all
    group members'''
    group_answers = groups_answers.split('\n')
    all_yeses = set(string.ascii_lowercase)
    for person_answers in group_answers:
        all_yeses = set(person_answers) & all_yeses
    total_all_yeses += len(all_yeses)


print(f'Solution to part 1. Sum of counts is {total_yeses}.')
print(f'Solution to part 2. Sum of counts is {total_all_yeses}.')
