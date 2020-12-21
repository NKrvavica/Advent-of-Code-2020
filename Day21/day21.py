# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 08:21:39 2020

@author: Nino
"""

from collections import defaultdict

def load_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n')
    return data


def parse_data(data):
    menu = []
    for line in data:
        ingred_set, allerg_set = [], []
        ingred, allerg = line.split(' (contains ')
        allerg = allerg.replace(')','')
        for i in ingred.split(' '):
            ingred_set.append(i)
        for a in allerg.split(', '):
            allerg_set.append(a)
        menu.append((ingred_set, allerg_set))
    return menu


def find_all_possible_allergen_ingredients(menu):
    allergens = defaultdict()
    for meal in menu:
        ingrid, allerg = meal
        for a in allerg:
            if a in allergens:
                allergens[a] = allergens[a].intersection(ingrid)
            else:
                allergens[a] = set(ingrid)
    return allergens


def find_dangerous_ingredients(combinations):
    dangerous_ingredients = set()
    allergens = set(combinations.keys())
    known_allergens = defaultdict()
    while len(known_allergens) < len(allergens):
        for known_allergen, known_ingredients in combinations.items():
            if len(known_ingredients) == 1:
                known_ingredient = next(iter(known_ingredients))
                known_allergens[known_allergen] = known_ingredient
                dangerous_ingredients.update([known_ingredient])
                for allergen, ingrid in combinations.items():
                    if allergen != known_allergen:
                        combinations[allergen] = ingrid.difference(known_ingredients)
    return dangerous_ingredients, known_allergens


def count_allergofree_ingredients(menu, dangerous_ingredients):
    counter = 0
    for meal in menu:
        ingrid, allerg = meal
        for i in ingrid:
            if i not in dangerous_ingredients:
                counter += 1
    return counter


data = load_input('input.txt')
menu = parse_data(data)
combinations = find_all_possible_allergen_ingredients(menu)
dangerous_ingredients, known_allergens = find_dangerous_ingredients(combinations)

# part 1
p1 = count_allergofree_ingredients(menu, dangerous_ingredients)
print(f'Solution to part 1: {p1}')

# part 2
result_str = ''
sorted_allergens = sorted(known_allergens.items(), key=lambda x: (x[0]))
for i, (allergen, ingrid) in enumerate(sorted_allergens):
    result_str = result_str + ingrid + ','
print(f'Solution to part 2: {result_str[:-1]}')
