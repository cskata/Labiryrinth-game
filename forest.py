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
    'EDGE': [1, '\u2588\u2588'],
    'SPAWNED_ITEM': [2, '\U0001F333', 8]
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


def print_forest(forest):
    os.system('clear')
    forest = common.import_lab_level("forest")
    for x, row in enumerate(forest):
        for y, cell in enumerate(row):
            for k in FOREST_ITEMS.keys():
                if FOREST_ITEMS[k][0] == forest[x][y]:
                    key = k
            if forest[x][y] == FOREST_ITEMS[key][0]:
                sys.stdout.write(FOREST_ITEMS[key][1])
        print()


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


def spawn_enemies():
    pass


def main():
    forest = spawn_trees()
    print_forest(forest)


if __name__ == '__main__':
    main()
