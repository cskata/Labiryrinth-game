import csv
import os
import sys
import termios
import time
import tty

import lab_generator
import main_title


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
        time.sleep(0.06)


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


def what_the_witch_say_in_cellar(sweets_to_collect):
    pass
