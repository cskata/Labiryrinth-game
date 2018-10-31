import os
import sys
import time
from common import getch
from cellar import CELLAR_ITEMS


title_l1 = r"""  _    _                      _                   _    _____          _       _ """
title_l2 = r""" | |  | |                    | |                 | |  / ____|        | |     | |"""
title_l3 = r""" | |__| | __ _ _ __  ___  ___| |   __ _ _ __   __| | | |  __ _ __ ___| |_ ___| |"""
title_l4 = r""" |  __  |/ _` | '_ \/ __|/ _ \ |  / _` | '_ \ / _` | | | |_ | '__/ _ \ __/ _ \ |"""
title_l5 = r""" | |  | | (_| | | | \__ \  __/ | | (_| | | | | (_| | | |__| | | |  __/ ||  __/ |"""
title_l6 = r""" |_|  |_|\__,_|_| |_|___/\___|_|  \__,_|_| |_|\__,_|  \_____|_|  \___|\__\___|_|"""

titles = [title_l1, title_l2, title_l3, title_l4, title_l5, title_l6]


def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.06)


def print_centered_main_title(title):
    for line in title:
        print("{: ^100s}".format(line))
    press_start = "Press any button to start the game."
    print("\n" * 2)
    print("{: ^100s}".format(press_start))
    start_game = False
    if getch():
        start_game = True


def print_centered_level_title(art):
    for line in art:
        print(line)
    print("\n")


def game_intro():
    os.system('clear')
    print_centered_main_title(titles)


def cellar_intro():
    os.system('clear')
    time.sleep(1)
    print_slow("\nHansel and Gretel got lost in the woods and the evil witch captured them.")
    print_slow("\nThey are locked in the witch's cellar. Help them to escape.")
    time.sleep(1)
    sweets_to_eat = CELLAR_ITEMS['SPAWNED_ITEM'][2]
    print_slow(f"\nThey have to eat {sweets_to_eat} sweets to open the gate below.")
    time.sleep(1)
    print_slow("\nYou can move by pressing WASD.")
    time.sleep(2)
    print('\n')
    print("When you are ready, press any button to begin.")
    start_game = False
    if getch():
        start_game = True


def cellar_outro():
    time.sleep(1)
    print_slow("\nHansel has gotten fat. He fell into the witch's oven. ")
    time.sleep(1)
    print_slow("Congratulations. You killed him!")
    time.sleep(2)
    print_slow("\nBut Gretel survived...")
    print_slow(" And she wants to avenge Hansel. You must help her!")
    time.sleep(1)
    print_slow("\n(And try not to kill her too... \U0001F620)\n")
    time.sleep(2)
    print("\nWhen you are ready, press any button to begin.")
    start_game = False
    if getch():
        start_game = True


def forest_intro():
    os.system('clear')
    time.sleep(1)
    print_slow("\nGretel escaped from the cellar, she is in the enchanted forest now.\n")
    time.sleep(1)
    print_slow("She has to find the magic sword to defeat the evil witch.\n")
    time.sleep(1)
    print_slow("The sword is hidden under a tree. \n")
    print_slow("Gretel has to chop down every tree until she finds the magic sword.\n\n")
    time.sleep(2)
    print("When you are ready, press any button to begin.")
    start_game = False
    if getch():
        start_game = True


def forest_outro():
    time.sleep(1)
    print_slow("\nGretel is now heading to the witch's hut.\n")
    time.sleep(1)
    print_slow("Suddenly she got very tired since she had to cut down so many trees.\n")
    time.sleep(1)
    print_slow("She lied down near the river to take a quick nap.\n")
    time.sleep(1)
    print_slow("Riiight next to the witch's hut. GG kid... \n")
    time.sleep(3)
    print_slow("\nTo Be Continued....\n")
    time.sleep(5)
