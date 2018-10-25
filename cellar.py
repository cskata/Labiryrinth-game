from termcolor import colored
import os
import random
import sys
import termios
import time
import tty

import lab_generator
import common
import forest

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
    'EXIT': [3, '\u2584\u2584', 'red'],
    'ENTRY': [4, '\u2580\u2580', 'red'],
    'PLAYER': [5, '\u265f ', 'blue']
    }


def place_and_close_gates(labyrinth):
    labyrinth[0][2] = CELLAR_ITEMS['ENTRY'][0]
    labyrinth[0][3] = CELLAR_ITEMS['ENTRY'][0]
    labyrinth[LAB_HEIGHT][LAB_WIDTH - 2] = CELLAR_ITEMS['EXIT'][0]
    labyrinth[LAB_HEIGHT][LAB_WIDTH - 1] = CELLAR_ITEMS['EXIT'][0]


def open_gates(labyrinth):
    labyrinth[LAB_HEIGHT][LAB_WIDTH - 2] = CELLAR_ITEMS['CORRIDOR'][0]
    labyrinth[LAB_HEIGHT][LAB_WIDTH - 1] = CELLAR_ITEMS['CORRIDOR'][0]


def create_cellar_with_sweets(spawned_sweets=0):
    lab_generator.main()
    labyrinth = common.import_lab_level("new_lab")
    sweets_to_spawn = CELLAR_ITEMS['SPAWNED_ITEM'][2]
    while spawned_sweets != sweets_to_spawn:
        x = random.randint(1, LAB_WIDTH)
        y = random.randint(1, LAB_HEIGHT)
        if labyrinth[x][y] == CELLAR_ITEMS['CORRIDOR'][0]:
            labyrinth[x][y] = CELLAR_ITEMS['SPAWNED_ITEM'][0]
            spawned_sweets += 1
        else:
            spawned_sweets += 0
    # exports the generated cellar with the random sweets to a new file
    # the labyrinth's matrix it wont be overwritten every time
    common.export_random_lab(labyrinth, "cellar")
    # then imports it back and returns the labyrinth
    # since the function is called only once, the function can have a return value
    labyrinth = common.import_lab_level("cellar")
    return labyrinth


def draw(labyrinth, collected_sweets, sweets_to_collect):
    os.system('clear')
    print_how_many_sweets_left(labyrinth, collected_sweets, sweets_to_collect)
    for x, row in enumerate(labyrinth):
        for y, cell in enumerate(row):
            # finding the the current element's (cell) key in CELLAR_ITEMS dict.
            # the key can be used as a variable so there is no need for many ifs
            for k in CELLAR_ITEMS.keys():
                if CELLAR_ITEMS[k][0] == labyrinth[x][y]:
                    key = k
            if CELLAR_ITEMS[key][0] > 2:
                if labyrinth[x][y] == CELLAR_ITEMS[key][0]:
                    sys.stdout.write(colored(CELLAR_ITEMS[key][1], CELLAR_ITEMS[key][2]))
            elif labyrinth[x][y] == CELLAR_ITEMS[key][0]:
                sys.stdout.write(CELLAR_ITEMS[key][1])
        print()


def count_uncollected_sweets(labyrinth, coll_sweets=0):
    sweets_to_coll = CELLAR_ITEMS['SPAWNED_ITEM'][2]
    for row in labyrinth:
        coll_sweets += row.count(2)
    uncoll_sweets = sweets_to_coll - coll_sweets
    return uncoll_sweets


def escaped_from_cellar(labyrinth, game_over=False):
    gate1 = labyrinth[LAB_HEIGHT][LAB_WIDTH - 2]
    gate2 = labyrinth[LAB_HEIGHT][LAB_WIDTH - 1]
    player = CELLAR_ITEMS['PLAYER'][0]
    if gate1 == player or gate2 == player:
        game_over = True
    return game_over


def print_how_many_sweets_left(labyrinth, colld_sw, sw_to_coll):
    if colld_sw != sw_to_coll:
        print(f"They must eat all the {sw_to_coll} sweets to escape through the gate below!\n")
    else:
        print("Hansel ate all the sweets. The gate is now open, they can escape!\n")
        open_gates(labyrinth)
    print("Hansel already ate {} sweet(s). Good.".format(colld_sw))
    print("He must eat {} more. Hurry-hurry!\n".format(sw_to_coll - colld_sw))


def init_new_cellar():
    labyrinth = create_cellar_with_sweets()
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
        labyrinth = common.move_player(labyrinth, CELLAR_ITEMS)
    draw(labyrinth, collected_sweets, sweets_to_collect)
    # common.cellar_outro()
    os.system('python3 forest.py')


if __name__ == '__main__':
    main()
