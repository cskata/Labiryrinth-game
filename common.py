import csv
import os
import sys
import termios
import time
import tty

import lab_generator
import introoutro


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.06)


def import_lab_level(filename="labyrinth_orig"):
    with open("{}.csv".format(filename), "r") as f:
        new_lab = list(csv.reader(f))
        for lst in new_lab:
            for i in range(0, len(lst), 1):
                lst[i] = int(lst[i])
        return new_lab


def export_random_lab(grid, filename="new_lab"):
    with open("{}.csv".format(filename), 'w+') as f:
        writer = csv.writer(f)
        for row in grid:
            writer.writerow(row)


def add_items_to_biom(x, y, biom, biom_dict):
    if biom[x][y] == biom_dict['CORRIDOR'][0]:
        biom[x][y] = biom_dict['SPAWNED_ITEM'][0]
        return 1
    else:
        return 0


def get_cells_key(x, y, biom, biom_dic):
    for k in biom_dic.keys():
        if biom_dic[k][0] == biom[x][y]:
            key = k
    return key


def find_player(labyrinth, biom):
    coordinates = []
    for x_coord, row in enumerate(labyrinth):
        for y_coord, item in enumerate(row):
            if item == biom['PLAYER'][0]:
                coordinates.append(x_coord)
                coordinates.append(y_coord)
    return coordinates


def move_player(labyrinth, biom):
    new_move = getch()
    x = find_player(labyrinth, biom)[0]
    y = find_player(labyrinth, biom)[1]
    labyrinth[x][y] = biom['CORRIDOR'][0]
    move_coords = {
        'w': [x - 1, y, 'ver'],
        'a': [x, y - 1, 'hor'],
        's': [x + 1, y, 'ver'],
        'd': [x, y + 1, 'hor']}

    # find move's index with dictionary
    if new_move in move_coords.keys():
        move_x = move_coords[new_move][0]
        move_y = move_coords[new_move][1]
        if labyrinth[move_x][move_y] == biom['SPAWNED_ITEM'][0]:
            labyrinth[move_x][move_y] = biom['CORRIDOR'][0]
        if labyrinth[move_x][move_y] == biom['CORRIDOR'][0]:
            if move_coords[new_move][2] == 'hor':
                y = move_y
            elif move_coords[new_move][2] == 'ver':
                x = move_x
    if new_move == "x":
        exit()
    labyrinth[x][y] = biom['PLAYER'][0]
    return labyrinth
