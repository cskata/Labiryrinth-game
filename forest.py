from termcolor import colored
import os
import random
import sys
import termios
import time
import tty

import lab_generator
import common

FOREST_WIDTH = 20
FOREST_HEIGTH = 20


FOREST_ITEMS = {
    'CORRIDOR': [0, ' '],
    'WALL': [1, '\u2588\u2588'],
    'SPAWNED_ITEM': [2, '\U0001F333', 8],
    'EXIT': [3, '\u2584\u2584', 'red'],
    'ENTRY': [4, '\u2580\u2580', 'red'],
    'PLAYER': [5, '\u25CF', 'yellow']
}


def create_forest_area():
    forest = []
    edge = ("1" * (FOREST_WIDTH) + "11")
    gameplay_area = ("1" + ("00" * (FOREST_WIDTH)) + "1")
    forest.append(edge)
    for _ in range(FOREST_HEIGTH):
        forest.append(gameplay_area)
    forest.append(edge)
    common.export_random_lab(forest, "forest")
    forest = common.import_lab_level("forest")
    return forest


def spawn_trees(spawned_trees=0):
    # find the tree where a sword is hidden
    trees_to_spawn = FOREST_ITEMS['SPAWNED_ITEM'][2]
    forest = create_forest_area()
    while spawned_trees != trees_to_spawn:
        x = random.randint(2, (FOREST_WIDTH - 1))
        y = random.randint(2, (FOREST_HEIGTH * 2))
        if forest[x][y - 1] == FOREST_ITEMS['CORRIDOR'][0]:
            if forest[x][y] == FOREST_ITEMS['CORRIDOR'][0]:
                forest[x][y] = FOREST_ITEMS['SPAWNED_ITEM'][0]
                forest[x].pop(y - 1)
                spawned_trees += 1
            else:
                spawned_trees += 0
    common.export_random_lab(forest, "forest")
    forest = common.import_lab_level("forest")
    return forest


def print_forest(forest):
    os.system('clear')
    for x, row in enumerate(forest):
        for y, cell in enumerate(row):
            for k in FOREST_ITEMS.keys():
                if FOREST_ITEMS[k][0] == forest[x][y]:
                    key = k
            if key == 'ENTRY' or key == 'EXIT' or key == 'PLAYER':
                if forest[x][y] == FOREST_ITEMS[key][0]:
                    sys.stdout.write(colored(FOREST_ITEMS[key][1], FOREST_ITEMS[key][2]))
            elif forest[x][y] == FOREST_ITEMS[key][0]:
                sys.stdout.write(FOREST_ITEMS[key][1])
        print()


def spawn_enemies():
    pass


def place_and_close_gates(forest):
    forest[0][2] = FOREST_ITEMS['ENTRY'][0]
    forest[0][3] = FOREST_ITEMS['ENTRY'][0]
    forest[(FOREST_HEIGTH) + 1][4] = FOREST_ITEMS['EXIT'][0]
    forest[(FOREST_HEIGTH) + 1][5] = FOREST_ITEMS['EXIT'][0]


def init_new_forest():
    forest = spawn_trees()
    place_and_close_gates(forest)
    forest[2][2] = FOREST_ITEMS['PLAYER'][0]
    return forest


def escaped_from_forest(forest, game_over=False):
    gate1 = forest[(FOREST_HEIGTH) + 1][4]
    gate2 = forest[(FOREST_HEIGTH) + 1][5]
    player = FOREST_ITEMS['PLAYER'][0]
    if gate1 == player or gate2 == player:
        game_over = True
    return game_over


def main():
    forest = init_new_forest()
    while not escaped_from_forest(forest):
        print_forest(forest)
        forest = common.move_player(forest, FOREST_ITEMS)


if __name__ == '__main__':
    main()
