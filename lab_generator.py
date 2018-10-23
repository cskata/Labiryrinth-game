from random import shuffle, randrange
import common

width = 12
height = 12
visited_cell = [[0] * width + [1] for _ in range(height)] + [[1] * (width + 1)]
ver = [["100"] * width + ['1'] for _ in range(height)] + [[]]
hor = [["111"] * width + ['1'] for _ in range(height + 1)]


def walk(x, y):
    visited_cell[y][x] = 1

    directions = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
    shuffle(directions)
    for (xx, yy) in directions:
        if visited_cell[yy][xx]:
            continue
        if xx == x:
            hor[max(y, yy)][x] = "100"
        if yy == y:
            ver[y][max(x, xx)] = "000"
        walk(xx, yy)


def join_rows_to_maze(hor, ver):
    full_maze = []
    maze_row = zip(hor, ver)
    for (a, b) in maze_row:
        full_maze.append((''.join(a)))
        full_maze.append((''.join(b)))
        full_maze.append((''.join(b)))
    return full_maze


def create_random_maze():
    walk(randrange(width), randrange(height))
    full_maze = join_rows_to_maze(hor, ver)
    full_maze.pop()
    return full_maze


def make_new_lab():
    labyrinth = create_random_maze()
    common.export_random_lab(labyrinth)
