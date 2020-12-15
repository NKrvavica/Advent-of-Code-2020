# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 08:40:39 2020

@author: Nino
"""

from time import time
from numba import njit
import numpy as np


@njit
def speak_given_numbers(given_numbers):
    spoken_numbers = {}
    for i, nr in enumerate(given_numbers):
        spoken_numbers[nr] = i+1
    return spoken_numbers, given_numbers[-1]


@njit
def play_the_game(start, spoken_numbers, last_spoken, end):
    for turn in range(start, end):
        if last_spoken in spoken_numbers:
            speak = turn - spoken_numbers[last_spoken]
        else: speak = 0
        spoken_numbers[last_spoken] = turn
        last_spoken = speak
    return spoken_numbers, last_spoken


msStart = time()

given_numbers = np.array([8,0,17,4,1,12])

spoken_numbers, last_spoken = speak_given_numbers(given_numbers)

spoken_numbers, last_spoken1 = play_the_game(6, spoken_numbers,
                                             last_spoken, 2020)

spoken_numbers, last_spoken2 = play_the_game(2020, spoken_numbers,
                                             last_spoken1, 30000000)

print(f'Solution to part 1: {last_spoken1}\n')
print(f'Solution to part 2: {last_spoken2}\n')
print(f'Run time: {time() - msStart:.2f} s')
