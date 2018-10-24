import csv
import os
import sys
import termios
import time
import tty

import lab_generator


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.05)


def import_lab_level(filename="labyrinth_orig"):
    with open("{}.csv".format(filename), "r") as f:
        new_lab = list(csv.reader(f))
        for lst in new_lab:
            for i in range(0, len(lst), 1):
                lst[i] = int(lst[i])
        return new_lab


def export_random_lab(grid, filename="new_lab"):
    with open("{}.csv".format(filename), 'w+') as f:
        writer = csv.writer(f)
        for row in grid:
            writer.writerow(row)


def game_intro():
    os.system('clear')
    print(r"""
  _    _                      _                   _    _____          _       _
 | |  | |                    | |                 | |  / ____|        | |     | |
 | |__| | __ _ _ __  ___  ___| |   __ _ _ __   __| | | |  __ _ __ ___| |_ ___| |
 |  __  |/ _` | '_ \/ __|/ _ \ |  / _` | '_ \ / _` | | | |_ | '__/ _ \ __/ _ \ |
 | |  | | (_| | | | \__ \  __/ | | (_| | | | | (_| | | |__| | | |  __/ ||  __/ |
 |_|  |_|\__,_|_| |_|___/\___|_|  \__,_|_| |_|\__,_|  \_____|_|  \___|\__\___|_|""")
    time.sleep(0.5)
    print_slow("\nHansel and Gretel got lost in the woods and the evil witch captured them.")
    print_slow("\nThey are locked in the witch's cellar. Help them to escape.\n")
    time.sleep(0.7)
    print("They have to eat 4 sweets to open the gate and escape.")
    time.sleep(1.2)
    print("You can move by pressing WASD.")
    time.sleep(1.2)
    print("When you are ready, press any button to start the game.")
    start_game = False
    if getch():
        start_game = True


def cellar_intro():
    pass


def cellar_outro():
    print_slow("\nHansel and Gretel has gotten fat! They walked right into the witch's oven.")
    time.sleep(1)
    print_slow(" Congratulations! You killed them!")
    print("\n")


def what_the_witch_say_in_cellar(sweets_to_collect):
    pass
