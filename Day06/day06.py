# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 09:30:05 2020

@author: Nino
"""


with open('input.txt') as f:
    declaration_form = f.read().split('\n\n')


total_yeses, total_all_yeses = 0, 0
for groups_answers in declaration_form:

    # part 1: number of questions that were answered yes
    group_answered_yes = set(groups_answers.replace('\n', ''))
    total_yeses += len(group_answered_yes)

    # part 2: questions that were answered yes by all group members
    all_yeses = group_answered_yes
    for person_answers in groups_answers.split('\n'):
        all_yeses &= set(person_answers)
    total_all_yeses += len(all_yeses)


print(f'Solution to part 1. Sum of counts is {total_yeses}.')
print(f'Solution to part 2. Sum of counts is {total_all_yeses}.')
