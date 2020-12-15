# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 08:40:39 2020

@author: Nino
"""

from time import time
from numba import njit
import numpy as np


@njit
def play_the_game(given_numbers, end):
    last_spoken = given_numbers[-1]
    spoken_numbers = {}
    for i, nr in enumerate(given_numbers):
        spoken_numbers[nr] = i+1
    for turn in range(len(given_numbers), end):
        if last_spoken in spoken_numbers:
            speak = turn - spoken_numbers[last_spoken]
        else: speak = 0
        spoken_numbers[last_spoken] = turn
        last_spoken = speak
    return last_spoken


msStart = time()

given_numbers = np.array([8,0,17,4,1,12])
last_spoken1 = play_the_game(given_numbers, 2020)
last_spoken2 = play_the_game(given_numbers, 30000000)

print(f'Solution to part 1: {last_spoken1}\n')
print(f'Solution to part 2: {last_spoken2}\n')
print(f'Run time: {time() - msStart:.2f} s')
