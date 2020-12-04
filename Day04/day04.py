# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 08:21:58 2020

@author: Nino
"""

import pandas as pd
import re


def parse_input(lines):
    passports = pd.DataFrame()
    for line in lines:
        line = line.replace('\n', ' ').split(' ')
        new_passport = {}
        for l in line:
            field, value = l.split(':')
            new_passport[field] = value
        passports = passports.append(new_passport, ignore_index=True)
    return passports


def is_hex(string):
    if re.search(r'^#(?:[0-9a-f]{3}){1,2}$', string):
        return True
    return False    



with open('input.txt') as f:
    lines = f.read().split('\n\n')

passports = parse_input(lines)

# part 1
passports.drop(['cid'], axis=1, inplace=True) # ignore 'cid'
valid_pass = passports[passports.isnull().sum(axis=1) == False]
print(f'Solution to part 1. Valid passports: {len(valid_pass)}')

# part 2
valid_pass = valid_pass.convert_dtypes()
num_columns = ['byr', 'iyr', 'eyr']
valid_pass[num_columns] = valid_pass[num_columns].apply(pd.to_numeric)

valid_pass = valid_pass[valid_pass['byr'].between(1920, 2002)]
valid_pass = valid_pass[valid_pass['iyr'].between(2010, 2020)]
valid_pass = valid_pass[valid_pass['eyr'].between(2020, 2030)]

valid_pass = valid_pass[valid_pass['hgt'].str.contains('cm|in', regex=True)]
valid_pass[['hgt_unit']] = valid_pass['hgt'].str[-2:]
valid_pass[['hgt_value']] = valid_pass['hgt'].str[:-2]
valid_pass['hgt_value'] = pd.to_numeric(valid_pass['hgt_value'])
valid_cm_height = ((valid_pass['hgt_value'].between(150, 193))
                   & (valid_pass['hgt_unit']=='cm'))
valid_in_height = ((valid_pass['hgt_value'].between(59, 76))
                   & (valid_pass['hgt_unit']=='in'))
valid_pass = valid_pass[valid_cm_height | valid_in_height]

valid_pass = valid_pass[[is_hex(hcl) for hcl in valid_pass['hcl']]]

valid_eye_colors = set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])
valid_pass = valid_pass[valid_pass['ecl'].isin(valid_eye_colors)]

valid_pass = valid_pass[valid_pass['pid'].str.len()==9]

print(f'Solution to part 2. Valid passports: {len(valid_pass)}')

