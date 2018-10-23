from termcolor import colored
import os
import random
import sys
import termios
import time
import tty

import lab_generator
import common

LAB_WIDTH = lab_generator.WIDTH * 3
LAB_HEIGHT = lab_generator.HEIGHT * 3


def collectable_sweets():
    BOLD = "\033[1m"
    END = "\033[0m"
    lolly = colored((f"{BOLD}{'@'}{END}"), "blue")
    pop = colored((f"{BOLD}{'-'}{END}"), "yellow")
    lollypop = lolly + pop
    return lollypop


# item: numbers in grid, char to print, other data if needed
ITEMS = {
    'CORRIDOR': [0, '  '],
    'WALL': [1, '\u2588\u2588'],
    'SPAWNED_ITEM': [2, collectable_sweets(), 1],
    'GATE': [3, '\u2588\u2588', 'red'],
    'PLAYER': [4, '\u2659\u265f']
    }


def add_sweets_and_gates(lab_width, lab_height, generated_keys=0):
    sweets = ITEMS['SPAWNED_ITEM'][2]
    lab_generator.make_new_lab()
    labyrinth = common.import_lab_level("new_lab")

    labyrinth[0][2] = ITEMS['GATE'][0]
    labyrinth[0][3] = ITEMS['GATE'][0]
    labyrinth[lab_height][lab_width - 2] = ITEMS['GATE'][0]
    labyrinth[lab_height][lab_width - 1] = ITEMS['GATE'][0]

    while generated_keys != sweets:
        key_a = random.randint(0, lab_height)
        key_b = random.randint(0, lab_width)
        if labyrinth[key_a][key_b] == 0:
            labyrinth[key_a][key_b] = 2
            generated_keys += 1
        else:
            generated_keys += 0

    common.export_random_lab(labyrinth, "lab_to_play.csv")


def draw(labyrinth):
    i = 0
    while i < len(labyrinth):
        j = 0
        while j < len(labyrinth[i]):
            if labyrinth[i][j] == ITEMS['WALL'][0]:
                sys.stdout.write(ITEMS['WALL'][1])
            elif labyrinth[i][j] == ITEMS['CORRIDOR'][0]:
                sys.stdout.write(ITEMS['CORRIDOR'][1])
            elif labyrinth[i][j] == ITEMS['PLAYER'][0]:
                sys.stdout.write(ITEMS['PLAYER'][1])
            elif labyrinth[i][j] == ITEMS['SPAWNED_ITEM'][0]:
                sys.stdout.write(ITEMS['SPAWNED_ITEM'][1])
            elif labyrinth[i][j] == ITEMS['GATE'][0]:
                sys.stdout.write(colored(ITEMS['GATE'][1], ITEMS['GATE'][2]))
            j = j + 1
        i = i + 1
        print()


def transpose_labyrinth(labyrinth):
    labyrinth = map(list, zip(*labyrinth))
    return labyrinth


def find_player(labyrinth):
    coordinates = []
    for id_i, row in enumerate(labyrinth):
        for id_j, item in enumerate(row):
            if item == ITEMS['PLAYER'][0]:
                coordinates.append(id_i)
                coordinates.append(id_j)
    return coordinates


def count_remaining_sweets(labyrinth):
    sweets_to_coll = ITEMS['SPAWNED_ITEM'][2]
    coll_sweets = 0
    for row in labyrinth:
        coll_sweets += row.count(2)
    uncoll_sweets = sweets_to_coll - coll_sweets
    return uncoll_sweets


def move_player(labyrinth):
    move = common.getch()
    i = find_player(labyrinth)[0]
    j = find_player(labyrinth)[1]
    labyrinth[i][j] = ITEMS['CORRIDOR'][0]
    if move == 'a':
        if labyrinth[i][j-1] == ITEMS['SPAWNED_ITEM'][0]:
            labyrinth[i][j-1] = ITEMS['CORRIDOR'][0]
        if labyrinth[i][j-1] == ITEMS['CORRIDOR'][0]:
            j = j - 1
    if move == 's':
        if labyrinth[i+1][j] == ITEMS['SPAWNED_ITEM'][0]:
            labyrinth[i+1][j] = ITEMS['CORRIDOR'][0]
        if labyrinth[i+1][j] == ITEMS['CORRIDOR'][0]:
            i = i + 1
    if move == 'd':
        if labyrinth[i][j+1] == ITEMS['SPAWNED_ITEM'][0]:
            labyrinth[i][j+1] = ITEMS['CORRIDOR'][0]
        if labyrinth[i][j+1] == ITEMS['CORRIDOR'][0]:
            j = j + 1
    if move == 'w':
        if labyrinth[i-1][j] == ITEMS['SPAWNED_ITEM'][0]:
            labyrinth[i-1][j] = ITEMS['CORRIDOR'][0]
        if labyrinth[i-1][j] == ITEMS['CORRIDOR'][0]:
            i = i - 1
    if move == "x":
        exit()
    labyrinth[i][j] = ITEMS['PLAYER'][0]
    return labyrinth


def game_over(labyrinth):
    game_over = False
    if labyrinth[LAB_HEIGHT][LAB_WIDTH - 1] == ITEMS['PLAYER'][0]:
        game_over = True
    elif labyrinth[LAB_HEIGHT][LAB_WIDTH - 2] == ITEMS['PLAYER'][0]:
        game_over = True
    return game_over


def main():
    common.game_intro()
    add_sweets_and_gates(LAB_WIDTH, LAB_HEIGHT)
    labyrinth = common.import_lab_level("lab_to_play")
    labyrinth[1][3] = ITEMS['PLAYER'][0]
    sweets_to_collect = ITEMS['SPAWNED_ITEM'][2]
    while not game_over(labyrinth):
        os.system('clear')
        coll_sweets = count_remaining_sweets(labyrinth)
        uncoll_sweets = sweets_to_collect - coll_sweets
        print("You already ate {} sweet(s). Good.".format(coll_sweets))
        print("You must eat {} more. Hurry-hurry!\n".format(uncoll_sweets))
        if coll_sweets == sweets_to_collect:
            labyrinth[LAB_HEIGHT][LAB_WIDTH - 2] = 0
            labyrinth[LAB_HEIGHT][LAB_WIDTH - 1] = 0
            print("You ate all the sweets. The gate is now open, you can escape!\n")
        draw(labyrinth)
        labyrinth = move_player(labyrinth)
    else:
        os.system('clear')
        draw(labyrinth)
        common.cellar_outro()
        # új szinthez ide kéne meghívni esetleg a következő szint mainjét?


if __name__ == '__main__':
    main()
