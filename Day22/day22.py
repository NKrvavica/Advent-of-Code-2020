# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 08:57:47 2020

@author: Nino
"""

from collections import deque
from itertools import islice
from time import time


def load_input(fname):
    with open(fname, 'r') as f:
        player1, player2 = f.read().split('\n\n')
    return player1, player2


def deal_cards(player):
    name, cards_str = player.split(':\n')
    return deque([int(card) for card in cards_str.split('\n')])


def play_game(deck1, deck2):
    while len(deck1)>0 and len(deck2)>0:
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if card1 > card2:
            deck1.extend([card1, card2])
        else:
            deck2.extend([card2, card1])
    return deck1, deck2, deck1 > deck2


def declare_winner(deck1, deck2, p1_won):
    winner_deck = [deck2, deck1][p1_won]
    winner_deck.reverse()
    return sum([i*card for i, card in enumerate(winner_deck, 1)])


player1, player2 = load_input('input.txt')
deck1, deck2 = deal_cards(player1), deal_cards(player2)
deck1_f, deck2_f, p1_won = play_game(deck1.copy(), deck2.copy())
part1 = declare_winner(deck1_f, deck2_f, p1_won)
print(f'Solution to part 1: {part1}')


# part 2
def play_recursive_game(deck1, deck2):
    deck1_seen, deck2_seen = [], []
    while deck1 and deck2:
        # print(deck1, deck2)
        if (deck1 in deck1_seen) or (deck2 in deck2_seen):
            return deck1, deck2, True
        else:
            deck1_seen.append(deck1.copy())
            deck2_seen.append(deck2.copy())
            card1, card2 = deck1.popleft(), deck2.popleft()
            if (len(deck1) >= card1) and (len(deck2) >= card2):
                # print(f'recursive game')
                card1_r = deque(islice(deck1, 0, card1))
                card2_r = deque(islice(deck2, 0, card2))
                p1d, p2d, p1_won = play_recursive_game(card1_r, card2_r)
                if p1_won == 1:
                    deck1.extend([card1, card2])
                else:
                    deck2.extend([card2, card1])
            else:
                if card1 > card2:
                    deck1.extend([card1, card2])
                else:
                    deck2.extend([card2, card1])
    return deck1, deck2, deck1 > deck2

msStart = time()

deck1_f, deck2_f, p1_won = play_recursive_game(deck1.copy(), deck2.copy())
part2 = declare_winner(deck1_f, deck2_f, p1_won)
print(f'Solution to part 2: {part2}')
print(f'Run time: {time() - msStart:.2f} s')

