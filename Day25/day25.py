# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 08:53:59 2020

@author: Nino
"""


def determine_loop_size(key, subject=7, value=1, divide_by=20201227):
    i = 0
    while value != key:
        i += 1
        value = (value * subject) % divide_by
    return i
       
        
def determine_encription_key(subject, loop_size, value=1, divide_by=20201227):
    for i in range(loop_size):
        value = (value * subject) % divide_by
    return value
        

card_public_key = 8184785
door_public_key = 5293040

card_loop_size = determine_loop_size(card_public_key)
door_loop_size = determine_loop_size(door_public_key)

encription_key = determine_encription_key(door_public_key, card_loop_size)

print(f'Encription key: {encription_key}')

