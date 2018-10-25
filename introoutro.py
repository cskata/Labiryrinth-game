import os
import sys
import time
import common

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


def print_centered_main_title():
    for title in titles:
        print("{: ^100s}".format(title))
    press_start = "Press any button to start the game."
    print("\n" * 3)
    print("{: ^100s}".format(press_start))
    start_game = False
    if common.getch():
        start_game = True


def game_intro():
    os.system('clear')
    main_title.print_centered_main_title()


def cellar_intro():
    os.system('clear')
    time.sleep(0.5)
    print_slow("\nHansel and Gretel got lost in the woods and the evil witch captured them.")
    print_slow("\nThey are locked in the witch's cellar. Help them to escape.\n")
    time.sleep(0.7)
    print("They have to eat 4 sweets to open the gate and escape.")
    time.sleep(1.2)
    print("You can move by pressing WASD.")
    time.sleep(1.2)
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
    print("\n")
    print_slow("But Gretel survived...")
    print_slow(" And she wants to avenge Hansel. You must help her!")
    time.sleep(1)
    print("\n")
    print_slow("(And try not to kill her too... \U0001F620)")
    print("\n")


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
    if common.getch():
        start_game = True
