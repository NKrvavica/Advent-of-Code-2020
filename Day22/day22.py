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
    cards = deque()
    for card in cards_str.split('\n'):
        cards.append(int(card))
    return cards


def play_game(p1_deck, p2_deck):
    while len(p1_deck)>0 and len(p2_deck)>0:
        p1_card = p1_deck.popleft()
        p2_card = p2_deck.popleft()
        if p1_card > p2_card:
            p1_deck.extend([p1_card, p2_card])
        else:
            p2_deck.extend([p2_card,p1_card])
    return p1_deck, p2_deck, p1_deck > p2_deck


def declare_winner(p1_deck, p2_deck, player1_won):
    if player1_won:
        winner_deck = p1_deck
    else:
        winner_deck = p2_deck
    winner_deck.reverse(),
    count = 0
    for i, card in enumerate(winner_deck, 1):
        count += i * card
    return count

player1, player2 = load_input('input.txt')
p1_deck, p2_deck = deal_cards(player1), deal_cards(player2)
p1_deck_f, p2_deck_f, player1_won = play_game(p1_deck.copy(), p2_deck.copy())
part1 = declare_winner(p1_deck_f, p2_deck_f, player1_won)
print(f'Solution to part 1: {part1}')


# part 2
def play_recursive_game(p1_deck, p2_deck):
    p1_previous, p2_previous = [], []
    while len(p1_deck)>0 and len(p2_deck)>0:
        # print(p1_deck, p2_deck)
        if (p1_deck in p1_previous) or (p2_deck in p2_previous):
            return p1_deck, p2_deck, True
        else:
            p1_previous.append(p1_deck.copy()), p2_previous.append(p2_deck.copy())
            p1_card = p1_deck.popleft()
            p2_card = p2_deck.popleft()
            if (len(p1_deck) >= p1_card) and (len(p2_deck) >= p2_card):
                # print(f'recursive game')
                p1d, p2d, player1_won = play_recursive_game(deque(islice(p1_deck.copy(), 0, p1_card)),
                                                            deque(islice(p2_deck.copy(), 0, p2_card)))
                if player1_won == 1:
                    p1_deck.extend([p1_card, p2_card])
                else:
                    p2_deck.extend([p2_card,p1_card])
            else:
                if p1_card > p2_card:
                    p1_deck.extend([p1_card, p2_card])
                else:
                    p2_deck.extend([p2_card,p1_card])
    return p1_deck, p2_deck, p1_deck > p2_deck

msStart = time()

p1_deck_f, p2_deck_f, player1_won = play_recursive_game(p1_deck.copy(), p2_deck.copy())
part2 = declare_winner(p1_deck_f, p2_deck_f, player1_won)
print(f'Solution to part 2: {part2}')
print(f'Run time: {time() - msStart:.2f} s')

