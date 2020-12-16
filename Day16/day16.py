# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 07:32:33 2020

@author: Nino
"""

import re
import numpy as np
from collections import defaultdict
from time import time


# =============================================================================
# FUNCTIONS
# =============================================================================

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


def find_valid_tickets(ticket_fields, nearby_tickets):
    all_valid_field_values = set.union(*ticket_fields.values())
    valid_tickets = []
    invalid_sum = 0
    for ticket in nearby_tickets:
        not_posibru = list(set(ticket).difference(all_valid_field_values))
        if not_posibru: invalid_sum += sum(not_posibru)
        else: valid_tickets.append(ticket)
    return valid_tickets, invalid_sum


def connect_values_with_ticket_fields(ticket_fields, valid_tickets):
     # numpy, yay! I can just transpose the matrix
    valid_tickets = np.array(valid_tickets)

    # find which number indices are valid for each field
    valid_idx = defaultdict(set)
    for idx, list_of_numbers in enumerate(valid_tickets.T):
        for field, valid_range in ticket_fields.items():
            if set(list_of_numbers).issubset(valid_range):
                valid_idx[field].add(idx)
    
    # find which field value corresponds to which index
    sorted_valid_idx = sorted(valid_idx.items(), key=lambda x: x[1])
    not_it = set()
    for field, idx in sorted_valid_idx:
        valid_idx[field] = valid_idx[field].difference(not_it)
        not_it.update(idx)
    
    return valid_idx


def define_my_ticket(valid_idx):
    my_prod = 1   
    for field, idx in valid_idx.items():
        if field[:6] == 'depart':
            my_prod *= my_ticket[list(idx)[0]]
    return my_prod


# =============================================================================
# MAIN
# =============================================================================

msStart = time()
data = load_input('input.txt')
ticket_fields, my_ticket, nearby_tickets = parse_input(*data)
valid_tickets, invalid_sum = find_valid_tickets(ticket_fields, nearby_tickets)
valid_idx = connect_values_with_ticket_fields(ticket_fields, valid_tickets)
my_prod = define_my_ticket(valid_idx)

print(f'Solution to part 1: {invalid_sum}')
print(f'Solution to part 2: {my_prod}')
print(f'Run time: {time() - msStart:.3f} s')
