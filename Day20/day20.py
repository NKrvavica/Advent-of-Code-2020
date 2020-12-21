# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 10:35:14 2020

@author: Nino
"""

import numpy as np
from time import time

msStart = time()


# =============================================================================
# FUNCTIONS
# =============================================================================
def load_input(fname):
    with open(fname, 'r') as f:
        data = f.read().split('\n\n')
    return data


def tile_edges(tiles_input):
    tiles = {}
    for tile in tiles_input:
        new_tile = []
        tile = tile.split('\n')
        _, tile_id = tile[0].split(' ')
        for line in tile[1:]:
            # new_tile.append(list(line.replace('.', '0').replace('#', '1')))
            new_tile.append(list(line))
        upper_edge = ''.join(new_tile[0])
        lower_edge = ''.join(new_tile[-1])
        rotated_tile = [[x[i] for x in new_tile] for i in range(len(new_tile[0]))]
        left_edge = ''.join(rotated_tile[0])
        right_edge = ''.join(rotated_tile[-1])
        tiles[tile_id[:-1]] = {'upper':upper_edge, 'lower':lower_edge,
                          'left': left_edge, 'right':right_edge}
    return tiles


def connect_edges(tiles):

    available_edges = {}
    for key, value in tiles.items():
        # print(key, value)
        available_edges[key] = set(value.keys())

    tiles_not_connected = set(tiles.keys())
    base_tiles = list([tiles_not_connected.pop()])
    connections = []
    while tiles_not_connected:
        batch_of_tiles = tiles_not_connected.copy()
        matched = []
        for second_tile in batch_of_tiles:
            # print(second_tile)
            all_edges = tiles[second_tile]
            # print(base_edge_loc)
            for edge_loc, edge in all_edges.items():
                for base_tile in base_tiles:
                    for base_edge_loc in available_edges[base_tile]:
                        if (edge == tiles[base_tile][base_edge_loc]): # normal of flipped edge
                            matched.append((second_tile, edge_loc))
                            matched.append((base_tile, base_edge_loc))
                            # print(f'{second_tile} na {base_tile}')
                            connections.append([second_tile, False, edge_loc, base_tile])
                            break
                        if (edge[::-1] == tiles[base_tile][base_edge_loc]): # normal of flipped edge
                            matched.append((second_tile, edge_loc))
                            matched.append((base_tile, base_edge_loc))
                            # print(f'{second_tile} na {base_tile}')
                            connections.append([second_tile, True,  edge_loc, base_tile])
                            break
                    else: continue
                    break
        for tile, loc in matched:
            if tile in tiles_not_connected:
                tiles_not_connected.remove(tile)
            if tile not in base_tile:
                base_tiles.append(tile)
            if tile in available_edges:
                if loc in available_edges[tile]:
                    available_edges[tile].remove(loc)
            if tile in batch_of_tiles:
                batch_of_tiles.remove(tile)

    return available_edges, tiles, connections


def get_tiles(tiles_input):
    tiles = {}
    for tile in tiles_input:
        new_tile = []
        tile = tile.split('\n')
        _, tile_id = tile[0].split(' ')
        for line in tile[1:]:
            new_tile.append(list(line.replace('.', '0').replace('#', '1')))
        tiles[tile_id[:-1]] = np.array(new_tile, dtype=np.int32)
    return tiles


def connect_tiles(tiles, connections):
    first_tile = connections[0][-1]
    tiles_positions ={first_tile: (0, 0)}
    tiles_rotated = {}
    tiles_rotated[first_tile] = tiles[first_tile]
    for ii, (second_id, flipped, edge, first_id) in enumerate(connections):

        upper = tiles_rotated[first_id][0, :]
        left = tiles_rotated[first_id][:, 0]
        lower = tiles_rotated[first_id][-1, :]
        right = tiles_rotated[first_id][:, -1]

        second_tile = tiles[second_id]

        matched = False
        if not matched: # lower - upper
            for i in range(8):
                second_edge = second_tile[-1, :] # donji rub
                if (second_edge == upper).all():
                    second_pos = (tiles_positions[first_id][0]-1,
                                  tiles_positions[first_id][1])
                    tiles_positions[second_id] = second_pos
                    tiles_rotated[second_id] = second_tile
                    matched = True
                    break
                second_tile = np.rot90(second_tile)
                if i == 3:
                    second_tile = np.fliplr(second_tile)
            second_tile = np.fliplr(second_tile)

        if not matched: # left - right
            for i in range(8):
                second_edge = second_tile[:, 0] # lijevi rub
                if (second_edge == right).all():
                    second_pos = (tiles_positions[first_id][0],
                                  tiles_positions[first_id][1]+1)
                    tiles_positions[second_id] = second_pos
                    tiles_rotated[second_id] = second_tile
                    matched = True
                    break
                second_tile = np.rot90(second_tile)
                if i == 3:
                    second_tile = np.fliplr(second_tile)
            second_tile = np.fliplr(second_tile)

        if not matched: # upper - lower
            for i in range(8):
                second_edge = second_tile[0, :] # gornji rub
                if (second_edge == lower).all():
                    second_pos = (tiles_positions[first_id][0]+1,
                                  tiles_positions[first_id][1])
                    tiles_positions[second_id] = second_pos
                    tiles_rotated[second_id] = second_tile
                    matched = True
                    break
                second_tile = np.rot90(second_tile)
                if i == 3:
                    second_tile = np.fliplr(second_tile)
            second_tile = np.fliplr(second_tile)

        if not matched: # right - left
            for i in range(8):
                second_edge = second_tile[:, -1] # desni rub
                if (second_edge == left).all():
                    second_pos = (tiles_positions[first_id][0],
                                  tiles_positions[first_id][1]-1)
                    tiles_positions[second_id] = second_pos
                    tiles_rotated[second_id] = second_tile
                    matched = True
                    break
                second_tile = np.rot90(second_tile)
                if i == 3:
                    second_tile = np.fliplr(second_tile)
            second_tile = np.fliplr(second_tile)
    return tiles_positions, tiles_rotated


def contruct_big_picture(tiles_positions, tiles_rotated):
    nr_of_tiles = len(tiles_positions.keys())
    rows_cols = int(np.sqrt(nr_of_tiles))  #number tiles in each row and colum
    tlen = len(tiles_rotated[next(iter(tiles_rotated))]) # size of each tile in x and y dir
    tln = tlen - 2 # size of each tiles without borders
    sorted_positions = sorted(tiles_positions.items(), key=lambda x: x[1])
    big_pic = np.zeros((rows_cols * tln, rows_cols * tln))
    for i in range(rows_cols):
        for j in range(rows_cols):
            tile_id, pos = sorted_positions[i*rows_cols+j]
            big_pic[i*tln:i*tln+tln, j*tln:j*tln+tln] = tiles_rotated[tile_id][1:-1, 1:-1]
    return big_pic


def construct_sea_monster(sea_monster_str):
    sea_monster = []
    for sm in sea_monster_str.split('\n'):
        sea_monster.append(list(sm.replace('.', '0').replace('#', '1')))
    sea_monster = np.array(sea_monster, dtype=np.int32)
    return sea_monster


def find_sea_monster(big_picture, sea_monster):
    monster_size = np.shape(sea_monster)
    counter = 0
    for i in range(4):
        for i in range(len(big_picture) - monster_size[0]):
            for j in range(len(big_picture) - monster_size[1]):
                cut = big_picture[i:i+monster_size[0], j:j+monster_size[1]]
                cut = np.array(cut, dtype=np.int32)
                if ((cut * sea_monster) == sea_monster).all():
                    counter += 1
            big_picture = np.fliplr(big_picture)
            for j in range(len(big_picture) - monster_size[1]):
                cut = big_picture[i:i+monster_size[0], j:j+monster_size[1]]
                cut = np.array(cut, dtype=np.int32)
                if ((cut * sea_monster) == sea_monster).all():
                    counter += 1
        big_picture = np.fliplr(big_picture)
        big_picture = np.rot90(big_picture)
    return counter



# =============================================================================
# MAIN
# =============================================================================

# part 1
tiles_input = load_input('input.txt')
tiles = tile_edges(tiles_input)
available_edges, tiles, connections = connect_edges(tiles)
p1 = 1
for key, value in available_edges.items():
    if len(value) == 2:
        p1 *= int(key)
print(f'Solution to part 1: {p1}')

# part 2
tiles = get_tiles(tiles_input)
tiles_positions, tiles_rotated = connect_tiles(tiles, connections)
big_picture = contruct_big_picture(tiles_positions, tiles_rotated)

#find sea monster
sea_monster_str = """..................#.
#....##....##....###
.#..#..#..#..#..#..."""
sea_monster = construct_sea_monster(sea_monster_str)
how_many_monsters = find_sea_monster(big_picture, sea_monster)

p2 = np.sum(big_picture) - how_many_monsters*np.sum(sea_monster)
print(f'Solution to part 2: {int(p2)}')

print(f'Run time: {time() - msStart:.2f} s')

# import matplotlib.pyplot as plt
# plt.imshow(big_pic)
