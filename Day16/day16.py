# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 07:32:33 2020

@author: Nino
"""

import re
import numpy as np
from collections import defaultdict

def load_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n\n')
    return data


def parse_input(fields, my_ticket, nearby_tickets):
    # get fields, and valid ranges
    valid_fields = {}
    for field in fields.split('\n'):
        field_name, value_ranges = field.split(': ')
        value_ranges = list(map(int, re.findall(r'\d+', value_ranges)))
        set_of_values1 = set(range(value_ranges[0], value_ranges[1]+1))
        set_of_values2 = set(range(value_ranges[2], value_ranges[3]+1))
        valid_fields[field_name] = set_of_values1 | set_of_values2

    # get my ticket values
    _, list_of_strings = my_ticket.split('\n')
    my_ticket_numbers = list(map(int, list_of_strings.split(',')))

    # get nearby tickets
    ticket_numbers = []
    for ticket in nearby_tickets.split('\n'):
        extracted_tickets = list(map(int, re.findall(r'\d+', ticket)))
        if extracted_tickets: ticket_numbers.append(extracted_tickets)
    
    return valid_fields, my_ticket_numbers, ticket_numbers


data = load_input('input.txt')
fields, my_ticket, nearby_tickets = parse_input(*data)


# part 1
all_valid_field_values = set.union(*fields.values())
valid_tickets = []
p1 = 0
for ticket in nearby_tickets:
    diff = list(set(ticket).difference(all_valid_field_values))
    if diff: p1 += sum(diff)
    else: valid_tickets.append(ticket)


# part 2
valid_tickets = np.array(valid_tickets) # numpy, yay! I can just transpose the matrix

# find which number indices are valid for each field
valid_idx = defaultdict(set)
for nr, place in enumerate(valid_tickets.T):
    for key, valid_nr in fields.items():
        if set(place).issubset(valid_nr):
            valid_idx[key].add(nr)

# find which field value corresponds to which row
sorted_places = sorted(valid_idx.items(), key=lambda x: x[1])
not_it = set()
for key, value in sorted_places:
    valid_idx[key] = valid_idx[key].difference(not_it)
    not_it.update(value)

# finally! get numbers in departure fields from my ticket and multiply them
p2 = 1   
for key, idx in valid_idx.items():
    if key[:6] == 'depart':
        p2 *= my_ticket[list(idx)[0]]


print(f'Solution to part 1: {p1}')
print(f'Solution to part 2: {p2}')
