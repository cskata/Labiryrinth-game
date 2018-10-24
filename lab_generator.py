# This generates a random labyrinth using the recursive backtrack method.
from random import shuffle, randrange
import common

WIDTH = 3
HEIGHT = 3
visited_cells = [[0] * WIDTH + [1] for _ in range(HEIGHT)] + [[1] * (WIDTH + 1)]
# visited_cells is just a utily list that includes 0's and 1's, to track the already visited cells
horizontal_walls = [["111"] * WIDTH + ['1'] for _ in range(HEIGHT + 1)]
vertical_walls = [["100"] * WIDTH + ['1'] for _ in range(HEIGHT)] + [[]]


def walk(x, y):
    visited_cells[y][x] = 1

    north = (x - 1, y)
    south = (x + 1, y)
    east = (x, y + 1)
    west = (x, y - 1)

    directions = [north, east, south, west]
    shuffle(directions)
    for (directon_x, direction_y) in directions:
        if visited_cells[direction_y][directon_x]:
            continue
        # removes horizontal wall, "111" turns into "100"
        if directon_x == x:
            horizontal_walls[max(y, direction_y)][x] = "100"
        # removes vertical wall, "100" turns into "000"
        if direction_y == y:
            vertical_walls[y][max(x, directon_x)] = "000"
        walk(directon_x, direction_y)


def append_rows_to_maze(hor, ver):
    full_maze = []
    maze_row = zip(hor, ver)
    for (a, b) in maze_row:
        full_maze.append((''.join(a)))
        # vertical row must be appended twice for wide corridors
        full_maze.append((''.join(b)))
        full_maze.append((''.join(b)))
    return full_maze


def create_random_maze():
    walk(randrange(WIDTH), randrange(HEIGHT))
    full_maze = append_rows_to_maze(horizontal_walls, vertical_walls)
    full_maze.pop()
    return full_maze


def make_new_lab():
    labyrinth = create_random_maze()
    common.export_random_lab(labyrinth)


make_new_lab()
