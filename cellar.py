from termcolor import colored
import os
import random
import sys
import termios
import time
import tty

import introoutro
from lab_generator import make_new_lab, WIDTH
import common


cellar_l1 = r""" _______ _             _____     _ _ """
cellar_l2 = r"""|__   __| |           / ____|   | | |"""
cellar_l3 = r"""   | |  | |__   ___  | |     ___| | | __ _ _ __"""
cellar_l4 = r"""   | |  | '_ \ / _ \ | |    / _ \ | |/ _` | '__|"""
cellar_l5 = r"""   | |  | | | |  __/ | |___|  __/ | | (_| | |"""
cellar_l6 = r"""   |_|  |_| |_|\___|  \_____\___|_|_|\__,_|_|"""


cellar_art = [cellar_l1, cellar_l2, cellar_l3, cellar_l4, cellar_l5, cellar_l6]


# LAB_WIDTH must be the WIDTH in lab_generator * 3
LAB_WIDTH = WIDTH * 3
LAB_HEIGHT = LAB_WIDTH


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
    make_new_lab()
    labyrinth = common.import_lab_level("new_lab")
    sweets_to_spawn = CELLAR_ITEMS['SPAWNED_ITEM'][2]
    while spawned_sweets != sweets_to_spawn:
        x = random.randint(1, LAB_WIDTH)
        y = random.randint(1, LAB_HEIGHT)
        spawned_sweets += common.add_items_to_biom(x, y, labyrinth, CELLAR_ITEMS)
    # exports the generated cellar with the random sweets to a new file
    # the labyrinth's matrix it wont be overwritten every time
    common.export_random_lab(labyrinth, "cellar")
    # then imports it back and returns the labyrinth
    # since the function is called only once, the function can have a return value
    labyrinth = common.import_lab_level("cellar")
    return labyrinth


def draw(labyrinth, collected_sweets, sweets_to_collect):
    os.system('clear')
    introoutro.print_centered_level_title(cellar_art)
    print_how_many_sweets_left(labyrinth, collected_sweets, sweets_to_collect)
    for x, row in enumerate(labyrinth):
        for y, cell in enumerate(row):
            # finding the the current element's (cell) key in CELLAR_ITEMS dict.
            # the key can be used as a variable so there is no need for many ifs
            key = common.get_cells_key(x, y, labyrinth, CELLAR_ITEMS)
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


def escaped_from_cellar(labyrinth, level_completed=False):
    gate1 = labyrinth[LAB_HEIGHT][LAB_WIDTH - 2]
    gate2 = labyrinth[LAB_HEIGHT][LAB_WIDTH - 1]
    player = CELLAR_ITEMS['PLAYER'][0]
    if gate1 == player or gate2 == player:
        level_completed = True
    return level_completed


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
    introoutro.game_intro()
    introoutro.cellar_intro()
    labyrinth = init_new_cellar()
    sweets_to_collect = CELLAR_ITEMS['SPAWNED_ITEM'][2]
    while not escaped_from_cellar(labyrinth):
        collected_sweets = count_uncollected_sweets(labyrinth)
        draw(labyrinth, collected_sweets, sweets_to_collect)
        labyrinth = common.move_player(labyrinth, CELLAR_ITEMS)
    draw(labyrinth, collected_sweets, sweets_to_collect)
    introoutro.cellar_outro()
    os.system('python3 forest.py')


if __name__ == '__main__':
    main()
