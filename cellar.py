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
CELLAR_ITEMS = {
    'CORRIDOR': [0, '  '],
    'WALL': [1, '\u2588\u2588'],
    'SPAWNED_ITEM': [2, collectable_sweets(), 1],
    'GATE': [3, '\u2588\u2588', 'red'],
    'PLAYER': [4, '\u2659\u265f']
    }


def place_and_close_gates():
    pass


def open_gates():
    pass


def add_sweets_and_gates(lab_width, lab_height, generated_keys=0):
    sweets = CELLAR_ITEMS['SPAWNED_ITEM'][2]
    lab_generator.make_new_lab()
    labyrinth = common.import_lab_level("new_lab")

    labyrinth[0][2] = CELLAR_ITEMS['GATE'][0]
    labyrinth[0][3] = CELLAR_ITEMS['GATE'][0]
    labyrinth[lab_height][lab_width - 2] = CELLAR_ITEMS['GATE'][0]
    labyrinth[lab_height][lab_width - 1] = CELLAR_ITEMS['GATE'][0]

    while generated_keys != sweets:
        key_a = random.randint(0, lab_height)
        key_b = random.randint(0, lab_width)
        if labyrinth[key_a][key_b] == 0:
            labyrinth[key_a][key_b] = 2
            generated_keys += 1
        else:
            generated_keys += 0

    common.export_random_lab(labyrinth, "cellar")


def draw(labyrinth, collected_sweets, sweets_to_collect):
    os.system('clear')
    if collected_sweets != sweets_to_collect:
        print(f"Eat all the {sweets_to_collect} sweets and you can escape through the gate below!\n")
    else:
        print("You ate all the sweets. The gate is now open, you can escape!\n")
        open_gates()
    print_how_many_sweets_left(collected_sweets, sweets_to_collect)
    i = 0
    while i < len(labyrinth):
        j = 0
        while j < len(labyrinth[i]):
            if labyrinth[i][j] == CELLAR_ITEMS['WALL'][0]:
                sys.stdout.write(CELLAR_ITEMS['WALL'][1])
            elif labyrinth[i][j] == CELLAR_ITEMS['CORRIDOR'][0]:
                sys.stdout.write(CELLAR_ITEMS['CORRIDOR'][1])
            elif labyrinth[i][j] == CELLAR_ITEMS['PLAYER'][0]:
                sys.stdout.write(CELLAR_ITEMS['PLAYER'][1])
            elif labyrinth[i][j] == CELLAR_ITEMS['SPAWNED_ITEM'][0]:
                sys.stdout.write(CELLAR_ITEMS['SPAWNED_ITEM'][1])
            elif labyrinth[i][j] == CELLAR_ITEMS['GATE'][0]:
                sys.stdout.write(colored(CELLAR_ITEMS['GATE'][1], CELLAR_ITEMS['GATE'][2]))
            j = j + 1
        i = i + 1
        print()


def find_player(labyrinth):
    coordinates = []
    for id_i, row in enumerate(labyrinth):
        for id_j, item in enumerate(row):
            if item == CELLAR_ITEMS['PLAYER'][0]:
                coordinates.append(id_i)
                coordinates.append(id_j)
    return coordinates


def count_uncollected_sweets(labyrinth, coll_sweets=0):
    sweets_to_coll = CELLAR_ITEMS['SPAWNED_ITEM'][2]
    for row in labyrinth:
        coll_sweets += row.count(2)
    uncoll_sweets = sweets_to_coll - coll_sweets
    return uncoll_sweets


def move_player(labyrinth):
    move = common.getch()
    i = find_player(labyrinth)[0]
    j = find_player(labyrinth)[1]
    labyrinth[i][j] = CELLAR_ITEMS['CORRIDOR'][0]
    if move == 'a':
        if labyrinth[i][j-1] == CELLAR_ITEMS['SPAWNED_ITEM'][0]:
            labyrinth[i][j-1] = CELLAR_ITEMS['CORRIDOR'][0]
        if labyrinth[i][j-1] == CELLAR_ITEMS['CORRIDOR'][0]:
            j = j - 1
    if move == 's':
        if labyrinth[i+1][j] == CELLAR_ITEMS['SPAWNED_ITEM'][0]:
            labyrinth[i+1][j] = CELLAR_ITEMS['CORRIDOR'][0]
        if labyrinth[i+1][j] == CELLAR_ITEMS['CORRIDOR'][0]:
            i = i + 1
    if move == 'd':
        if labyrinth[i][j+1] == CELLAR_ITEMS['SPAWNED_ITEM'][0]:
            labyrinth[i][j+1] = CELLAR_ITEMS['CORRIDOR'][0]
        if labyrinth[i][j+1] == CELLAR_ITEMS['CORRIDOR'][0]:
            j = j + 1
    if move == 'w':
        if labyrinth[i-1][j] == CELLAR_ITEMS['SPAWNED_ITEM'][0]:
            labyrinth[i-1][j] = CELLAR_ITEMS['CORRIDOR'][0]
        if labyrinth[i-1][j] == CELLAR_ITEMS['CORRIDOR'][0]:
            i = i - 1
    if move == "x":
        exit()
    labyrinth[i][j] = CELLAR_ITEMS['PLAYER'][0]
    return labyrinth


def are_they_escaped_from_cellar(labyrinth):
    game_over = False
    if labyrinth[LAB_HEIGHT][LAB_WIDTH - 1] == CELLAR_ITEMS['PLAYER'][0]:
        game_over = True
    elif labyrinth[LAB_HEIGHT][LAB_WIDTH - 2] == CELLAR_ITEMS['PLAYER'][0]:
        game_over = True
    return game_over


def print_how_many_sweets_left(colld_sw, sw_to_coll):
    print("You already ate {} sweet(s). Good.".format(colld_sw))
    print("You must eat {} more. Hurry-hurry!\n".format(sw_to_coll - colld_sw))


def main():
    # common.game_intro()
    add_sweets_and_gates(LAB_WIDTH, LAB_HEIGHT)
    labyrinth = common.import_lab_level("cellar")
    labyrinth[1][3] = CELLAR_ITEMS['PLAYER'][0]
    sweets_to_collect = CELLAR_ITEMS['SPAWNED_ITEM'][2]
    while not are_they_escaped_from_cellar(labyrinth):
        collected_sweets = count_uncollected_sweets(labyrinth)
        draw(labyrinth, collected_sweets, sweets_to_collect)
        if collected_sweets == sweets_to_collect:
            labyrinth[LAB_HEIGHT][LAB_WIDTH - 2] = CELLAR_ITEMS['CORRIDOR'][0]
            labyrinth[LAB_HEIGHT][LAB_WIDTH - 1] = CELLAR_ITEMS['CORRIDOR'][0]
            draw(labyrinth, collected_sweets, sweets_to_collect)
        labyrinth = move_player(labyrinth)
    else:
        draw(labyrinth, collected_sweets, sweets_to_collect)
        # common.cellar_outro()
        # új szinthez ide kéne meghívni esetleg a következő szint mainjét?


if __name__ == '__main__':
    main()
