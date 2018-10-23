from termcolor import colored
import csv
import os
import random
import sys
import termios
import time
import tty

import lab_generator
import common

lab_width = lab_generator.width * 3
lab_height = lab_generator.height * 3


def add_sweets_and_gates(lab_width, lab_height, sweets=4, generated_keys=0):
    lab_generator.make_new_lab()
    labyrinth = common.import_lab_level("new_lab")

    labyrinth[0][2] = 3
    labyrinth[0][3] = 3
    labyrinth[lab_height][lab_width - 2] = 3
    labyrinth[lab_height][lab_width - 1] = 3

    while generated_keys != sweets:
        key_a = random.randint(0, lab_height)
        key_b = random.randint(0, lab_width)
        if labyrinth[key_a][key_b] == 0:
            labyrinth[key_a][key_b] = 2
            generated_keys += 1
        else:
            generated_keys += 0

    common.export_random_lab(labyrinth, "lab_to_play.csv")


def collectable_sweets():
    BOLD = "\033[1m"
    END = "\033[0m"
    lolly = colored((f"{BOLD}{'@'}{END}"), "blue")
    pop = colored((f"{BOLD}{'-'}{END}"), "yellow")
    lollypop = lolly + pop
    return lollypop


def draw(labyrinth):
    i = 0
    while i < len(labyrinth):
        j = 0
        while j < len(labyrinth[i]):
            if labyrinth[i][j] == 1:
                sys.stdout.write('\u2588\u2588')
            elif labyrinth[i][j] == 0:
                sys.stdout.write('  ')
            elif labyrinth[i][j] == 4:
                sys.stdout.write('\u2659\u265f')
            elif labyrinth[i][j] == 2:
                sys.stdout.write(collectable_sweets())
            elif labyrinth[i][j] == 3:
                sys.stdout.write(colored('\u2588\u2588', "red"))
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
            if item == 4:
                coordinates.append(id_i)
                coordinates.append(id_j)
    return coordinates


def collect_sweets():
    sweets_to_coll = 4
    coll_sweets = 0
    uncoll_sweets = 4
    pass


def move_player(labyrinth):
    move = common.getch()
    i = find_player(labyrinth)[0]
    j = find_player(labyrinth)[1]
    labyrinth[i][j] = 0
    if move == 'a':
        if labyrinth[i][j-1] == 2:
            coll_sweets += 1
            uncoll_sweets -= 1
            labyrinth[i][j-1] = 0
        if labyrinth[i][j-1] == 0:
            j = j - 1
    if move == 's':
        if labyrinth[i+1][j] == 2:
            coll_sweets += 1
            uncoll_sweets -= 1
            labyrinth[i+1][j] = 0
        if labyrinth[i+1][j] == 0:
            i = i + 1
    if move == 'd':
        if labyrinth[i][j+1] == 2:
            coll_sweets += 1
            uncoll_sweets -= 1
            labyrinth[i][j+1] = 0
        if labyrinth[i][j+1] == 0:
            j = j + 1
    if move == 'w':
        if labyrinth[i-1][j] == 2:
            coll_sweets += 1
            uncoll_sweets -= 1
            labyrinth[i-1][j] = 0
        if labyrinth[i-1][j] == 0:
            i = i - 1
    if move == "x":
        exit()
    labyrinth[i][j] = 4
    return labyrinth


def game_over(labyrinth):
    game_over = False
    if labyrinth[lab_height][lab_width - 1] == 4:
        game_over = True
    elif labyrinth[lab_height][lab_width - 2] == 4:
        game_over = True
    return game_over


def main():
    # common.game_intro()
    add_sweets_and_gates(lab_width, lab_height)
    labyrinth = common.import_lab_level("lab_to_play")
    sweets_to_coll = 4
    coll_sweets = 0
    uncoll_sweets = 4
    labyrinth[1][3] = 4
    while not game_over(labyrinth):
        os.system('clear')
        print("You already ate {} sweet(s). Good.".format(coll_sweets))
        print("You must eat {} more. Hurry-hurry!\n".format(uncoll_sweets))
        if coll_sweets == sweets_to_coll:
            labyrinth[lab_height][lab_width - 2] = 0
            labyrinth[lab_height][lab_width - 1] = 0
        draw(labyrinth)
        labyrinth = move_player(labyrinth)
        # labyrinth[i][j] = 0
        # move = common.getch()
        # if move == 'a':
        #     if labyrinth[i][j-1] == 2:
        #         coll_sweets += 1
        #         uncoll_sweets -= 1
        #         labyrinth[i][j-1] = 0
        #     if labyrinth[i][j-1] == 0:
        #         j = j - 1
        # if move == 's':
        #     if labyrinth[i+1][j] == 2:
        #         coll_sweets += 1
        #         uncoll_sweets -= 1
        #         labyrinth[i+1][j] = 0
        #     if labyrinth[i+1][j] == 0:
        #         i = i + 1
        # if move == 'd':
        #     if labyrinth[i][j+1] == 2:
        #         coll_sweets += 1
        #         uncoll_sweets -= 1
        #         labyrinth[i][j+1] = 0
        #     if labyrinth[i][j+1] == 0:
        #         j = j + 1
        # if move == 'w':
        #     if labyrinth[i-1][j] == 2:
        #         coll_sweets += 1
        #         uncoll_sweets -= 1
        #         labyrinth[i-1][j] = 0
        #     if labyrinth[i-1][j] == 0:
        #         i = i - 1
        # if move == "x":
        #     exit()
        # labyrinth[i][j] = 4
        os.system('clear')
    else:
        draw(labyrinth)
        common.cellar_outro()
        # új szinthez ide kéne meghívni esetleg a következő szint mainjét?


if __name__ == '__main__':
    main()
