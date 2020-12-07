# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 11:53:30 2020

@author: PC-KRVAVICA
"""

with open('input.txt') as f:
    rules = f.read().split('\n')


# build the bag
all_bags = {}
for rule in rules:
    rule = rule.replace(' bags', '')
    rule = rule.replace(' bag', '')
    rule = rule.replace('.', '')
    rule = rule.replace('no', '0')
    parent_bag, children_bags = rule.split(' contain ')
    all_bags[parent_bag] = []
    for bag in children_bags.split(', '):
        all_bags[parent_bag].append((int(bag[:2]), bag[2:]))
    all_bags['other'] = []
    all_bags['other.'] = []

# part 1
good_bags = set()
finished = False
while not finished:
    count = len(good_bags)
    for parent_bag in all_bags:
        for bag in all_bags[parent_bag]:
            if bag[1] == 'shiny gold' or bag[1] in good_bags:
                good_bags.add(parent_bag)
    if count == len(good_bags):
        finished = True

p1 = len(good_bags)

# part 2 (recursion)
def bag_inception(parent_bag):
    counter = 0
    for bag in all_bags[parent_bag]:
        counter += bag[0] + bag[0] * bag_inception(bag[1])
    return counter

p2 = bag_inception('shiny gold')


print(f'Solution to part 1: {p1}')
print(f'Solution to part 2: {p2}')
