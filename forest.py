from termcolor import colored
import os
import random
import sys
import termios
import time
import tty

import lab_generator
import common
import introoutro

FOREST_WIDTH = 20
FOREST_HEIGTH = FOREST_WIDTH


def custom_tree():
    BOLD = "\033[1m"
    END = "\033[0m"
    tree = (f"{BOLD}{'@'}{END}")
    return tree


FOREST_ITEMS = {
    'CORRIDOR': [0, ' '],
    'WALL': [1, '\u2588\u2588'],
    'SPAWNED_ITEM': [2, custom_tree(), 'green', 8],
    'EXIT': [3, '\u2584\u2584', 'red'],
    'ENTRY': [4, '\u2580\u2580', 'red'],
    'PLAYER': [5, '\u265f', 'red'],
    'MAGIC_SWORD': [6, custom_tree(), 'green', False]
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
    trees_to_spawn = FOREST_ITEMS['SPAWNED_ITEM'][3]
    forest = create_forest_area()
    while spawned_trees != trees_to_spawn:
        x = random.randint(2, (FOREST_WIDTH - 1))
        y = random.randint(2, (FOREST_HEIGTH * 2))
        spawned_trees += common.add_items_to_biom(x, y, forest, FOREST_ITEMS)
    common.export_random_lab(forest, "forest")
    forest = common.import_lab_level("forest")
    return forest


def draw_forest(forest):
    os.system('clear')
    is_sword_found(forest, FOREST_ITEMS)
    for x, row in enumerate(forest):
        for y, cell in enumerate(row):
            key = common.get_cells_key(x, y, forest, FOREST_ITEMS)
            if key != 'CORRIDOR' and key != 'WALL':
                if forest[x][y] == FOREST_ITEMS[key][0]:
                    sys.stdout.write(colored(FOREST_ITEMS[key][1], FOREST_ITEMS[key][2]))
            elif forest[x][y] == FOREST_ITEMS[key][0]:
                sys.stdout.write(FOREST_ITEMS[key][1])
        print()


def find_tree_coordinates(forest):
    tree_coordinates = []
    for x_coord, row in enumerate(forest):
        for y_coord, item in enumerate(row):
            if item == FOREST_ITEMS['SPAWNED_ITEM'][0]:
                tree_coordinates.append([x_coord, y_coord])
    return tree_coordinates


def place_magic_sword(forest):
    # the magic sword disguises itself as a tree
    tree_coordinates = find_tree_coordinates(forest)
    random.shuffle(tree_coordinates)
    sword_coords = tree_coordinates[0]
    if sword_coords == [2, 2]:
        sword_coords = tree_coordinates[1]
    sx = sword_coords[0]
    sy = sword_coords[1]
    forest[sx][sy] = FOREST_ITEMS['MAGIC_SWORD'][0]


def place_and_close_gates(forest):
    forest[0][2] = FOREST_ITEMS['ENTRY'][0]
    forest[0][3] = FOREST_ITEMS['ENTRY'][0]


def is_sword_found(forest, biom_dic):
    if not biom_dic['MAGIC_SWORD'][3]:
        print("Gretel has not found the magic sword yet. Keep looking.\n")
    else:
        print("Gretel found the magic sword!! Now she can try to defeat the witch.\n")


def init_new_forest():
    forest = spawn_trees()
    place_and_close_gates(forest)
    place_magic_sword(forest)
    forest[2][2] = FOREST_ITEMS['PLAYER'][0]
    return forest


def main():
    introoutro.forest_intro()
    forest = init_new_forest()
    while not FOREST_ITEMS['MAGIC_SWORD'][3]:
        draw_forest(forest)
        forest = common.move_player(forest, FOREST_ITEMS)
    draw_forest(forest)


if __name__ == '__main__':
    main()
