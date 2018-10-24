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


# item: numbers in grid, char to print, other data if needed w: \u265f
CELLAR_ITEMS = {
    'CORRIDOR': [0, '  '],
    'WALL': [1, '\u2588\u2588'],
    'SPAWNED_ITEM': [2, collectable_sweets(), 2],
    'GATE': [3, '\u2588\u2588', 'red'],
    'PLAYER': [4, '\u2659 ']
    }


def place_and_close_gates(labyrinth):
    labyrinth[0][2] = CELLAR_ITEMS['GATE'][0]
    labyrinth[0][3] = CELLAR_ITEMS['GATE'][0]
    labyrinth[LAB_HEIGHT][LAB_WIDTH - 2] = CELLAR_ITEMS['GATE'][0]
    labyrinth[LAB_HEIGHT][LAB_WIDTH - 1] = CELLAR_ITEMS['GATE'][0]


def open_gates(labyrinth):
    labyrinth[LAB_HEIGHT][LAB_WIDTH - 2] = CELLAR_ITEMS['CORRIDOR'][0]
    labyrinth[LAB_HEIGHT][LAB_WIDTH - 1] = CELLAR_ITEMS['CORRIDOR'][0]


def create_cellar_with_sweets(spawned_sweets=0):
    lab_generator.make_new_lab()
    labyrinth = common.import_lab_level("new_lab")
    sweets_to_spawn = CELLAR_ITEMS['SPAWNED_ITEM'][2]
    while spawned_sweets != sweets_to_spawn:
        x = random.randint(0, LAB_WIDTH)
        y = random.randint(0, LAB_HEIGHT)
        if labyrinth[x][y] == 0:
            labyrinth[x][y] = 2
            spawned_sweets += 1
        else:
            spawned_sweets += 0
    # exports the genertaed cellar with sweets to a new file so it wont be overwritten every time
    common.export_random_lab(labyrinth, "cellar")


def draw(labyrinth, collected_sweets, sweets_to_collect):
    os.system('clear')
    print_how_many_sweets_left(labyrinth, collected_sweets, sweets_to_collect)
    x = 0
    while x < len(labyrinth):
        y = 0
        while y < len(labyrinth[x]):
            if labyrinth[x][y] == CELLAR_ITEMS['WALL'][0]:
                sys.stdout.write(CELLAR_ITEMS['WALL'][1])
            elif labyrinth[x][y] == CELLAR_ITEMS['CORRIDOR'][0]:
                sys.stdout.write(CELLAR_ITEMS['CORRIDOR'][1])
            elif labyrinth[x][y] == CELLAR_ITEMS['PLAYER'][0]:
                sys.stdout.write(CELLAR_ITEMS['PLAYER'][1])
            elif labyrinth[x][y] == CELLAR_ITEMS['SPAWNED_ITEM'][0]:
                sys.stdout.write(CELLAR_ITEMS['SPAWNED_ITEM'][1])
            elif labyrinth[x][y] == CELLAR_ITEMS['GATE'][0]:
                sys.stdout.write(colored(CELLAR_ITEMS['GATE'][1], CELLAR_ITEMS['GATE'][2]))
            y = y + 1
        x = x + 1
        print()


def find_player(labyrinth):
    coordinates = []
    for x_coord, row in enumerate(labyrinth):
        for y_coord, item in enumerate(row):
            if item == CELLAR_ITEMS['PLAYER'][0]:
                coordinates.append(x_coord)
                coordinates.append(y_coord)
    return coordinates


def count_uncollected_sweets(labyrinth, coll_sweets=0):
    sweets_to_coll = CELLAR_ITEMS['SPAWNED_ITEM'][2]
    for row in labyrinth:
        coll_sweets += row.count(2)
    uncoll_sweets = sweets_to_coll - coll_sweets
    return uncoll_sweets


def move_player(labyrinth):
    new_move = common.getch()
    x = find_player(labyrinth)[0]
    y = find_player(labyrinth)[1]
    labyrinth[x][y] = CELLAR_ITEMS['CORRIDOR'][0]
    move_coords = {
        'w': [x - 1, y, 'ver'],
        'a': [x, y - 1, 'hor'],
        's': [x + 1, y, 'ver'],
        'd': [x, y + 1, 'hor']}

    # find move's index with dictionary
    if new_move in move_coords.keys():
        cx = move_coords[new_move][0]
        cy = move_coords[new_move][1]
        if labyrinth[cx][cy] == CELLAR_ITEMS['SPAWNED_ITEM'][0]:
            labyrinth[cx][cy] = CELLAR_ITEMS['CORRIDOR'][0]
        if labyrinth[cx][cy] == CELLAR_ITEMS['CORRIDOR'][0]:
            if move_coords[new_move][2] == 'hor':
                y = cy
            elif move_coords[new_move][2] == 'ver':
                x = cx
    if new_move == "x":
        exit()
    labyrinth[x][y] = CELLAR_ITEMS['PLAYER'][0]
    return labyrinth


def escaped_from_cellar(labyrinth, game_over=False):
    gate1 = labyrinth[LAB_HEIGHT][LAB_WIDTH - 2]
    gate2 = labyrinth[LAB_HEIGHT][LAB_WIDTH - 1]
    player = CELLAR_ITEMS['PLAYER'][0]
    if gate1 == player or gate2 == player:
        game_over = True
    return game_over


def print_how_many_sweets_left(labyrinth, colld_sw, sw_to_coll):
    if colld_sw != sw_to_coll:
        print(f"Eat all the {sw_to_coll} sweets and you can escape through the gate below!\n")
    else:
        print("You ate all the sweets. The gate is now open, you can escape!\n")
        open_gates(labyrinth)
    print("You already ate {} sweet(s). Good.".format(colld_sw))
    print("You must eat {} more. Hurry-hurry!\n".format(sw_to_coll - colld_sw))


def init_new_cellar():
    create_cellar_with_sweets()
    labyrinth = common.import_lab_level("cellar")
    place_and_close_gates(labyrinth)
    labyrinth[1][3] = CELLAR_ITEMS['PLAYER'][0]
    return labyrinth


def main():
    # common.game_intro()
    # common.cellar_intro()
    labyrinth = init_new_cellar()
    sweets_to_collect = CELLAR_ITEMS['SPAWNED_ITEM'][2]
    while not escaped_from_cellar(labyrinth):
        collected_sweets = count_uncollected_sweets(labyrinth)
        draw(labyrinth, collected_sweets, sweets_to_collect)
        labyrinth = move_player(labyrinth)
    draw(labyrinth, collected_sweets, sweets_to_collect)
    # common.cellar_outro()
    # új szinthez ide kéne meghívni esetleg a következő szint mainjét?


if __name__ == '__main__':
    main()
