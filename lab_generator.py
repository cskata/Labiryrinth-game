# This generates a random labyrinth using the recursive backtrack method.
from random import shuffle, randrange
import common

width = 12
height = 12
visited_cell = [[0] * width + [1] for _ in range(height)] + [[1] * (width + 1)]
# visited_cell is just a utily list that includes 0's and 1's, to track the already visited cells
vertical_row = [["100"] * width + ['1'] for _ in range(height)] + [[]]
horizontal_row = [["111"] * width + ['1'] for _ in range(height + 1)]


def walk(x, y):
    visited_cell[y][x] = 1

    north = (x - 1, y)
    south = (x + 1, y)
    east = (x, y + 1)
    west = (x, y - 1)

    directions = [north, east, south, west]
    shuffle(directions)
    for (directon_x, direction_y) in directions:
        if visited_cell[direction_y][directon_x]:
            continue
        if directon_x == x:
            horizontal_row[max(y, direction_y)][x] = "100"
        if direction_y == y:
            vertical_row[y][max(x, directon_x)] = "000"
        walk(directon_x, direction_y)


def append_rows_to_maze(hor, ver):
    full_maze = []
    maze_row = zip(hor, ver)
    for (a, b) in maze_row:
        full_maze.append((''.join(a)))
        full_maze.append((''.join(b)))
        full_maze.append((''.join(b)))    # vertical row must be appended twice for wide corridors
    return full_maze


def create_random_maze():
    walk(randrange(width), randrange(height))
    full_maze = append_rows_to_maze(horizontal_row, vertical_row)
    full_maze.pop()
    return full_maze


def make_new_lab():
    labyrinth = create_random_maze()
    common.export_random_lab(labyrinth)


maze = create_random_maze()
print(maze)
