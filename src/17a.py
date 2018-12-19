from file_importer import FileImporter
from aoc_utils import Vector2
from collections import defaultdict
from enum import Enum
from queue import Queue
import re
import time

class DIRECTIONS(Enum):
    UP = Vector2(0, -1)
    RIGHT = Vector2(1, 0)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)

# Get input, create grid
inp = FileImporter.get_input("/../input/17.txt").split("\n")
grid = defaultdict(lambda: '.')

# Fill grid with walls
for i in inp:
    groups = re.match('([xy])=(.+), ([xy])=(.+)\.\.(.+)', i).groups()

    first = int(groups[1])
    second_min = int(groups[3])
    second_max = int(groups[4])

    for i in range(second_min, second_max + 1):
        if groups[0] == 'x':
            grid[(i, first)] = '#'
        else:
            grid[(first, i)] = '#'

ymax = max(grid.keys(), key = lambda x: x[0])[0]
ymin = min(grid.keys(), key = lambda x: x[0])[0]
xmax = max(grid.keys(), key = lambda x: x[1])[1]
xmin = min(grid.keys(), key = lambda x: x[1])[1]

# Put the spout
grid[(0, 500)] = '+'

def print_grid_around_cursor(grid, cursor):
    print('\n'*50)
    for y in range(cursor.y - 50, cursor.y + 50):
        for x in range(cursor.x - 50, cursor.x + 50):
            if Vector2(x, y) == cursor:
                print('O', end="")
                continue
            print(grid[(y, x)], end="")
        print()

def print_grid(grid):
    print('\n'*50)
    for y in range(ymin, ymax + 1):
        for x in range(xmin - 1, xmax + 2):
            print(grid[(y, x)], end="")
        print()

def fill_left_right_get_new_cursors(grid, cursor): 
    ''' Fill the spaces to the left/right, return an array of new cursors '''
    left_cursor = cursor + DIRECTIONS.LEFT.value
    right_cursor = cursor + DIRECTIONS.RIGHT.value

    # Cursors that were created as a part of this process. 
    # Cursors are created when water flows off an edge.
    new_cursors = []

    while True:
        left_grid_item = grid[left_cursor.to_yx_tuple()]

        if left_grid_item == '|':
            left_cursor = left_cursor + DIRECTIONS.LEFT.value
            continue

        # Wall
        if left_grid_item == '#':
            break

        # Open space
        if left_grid_item == '.':
            under_left_grid_item = grid[(left_cursor + DIRECTIONS.DOWN.value).to_yx_tuple()]

            if under_left_grid_item in '~#':
                grid[(left_cursor.to_yx_tuple())] = '|'
                left_cursor = left_cursor + DIRECTIONS.LEFT.value
                continue
            
            elif under_left_grid_item == '.':
                new_cursors.append(left_cursor)
                break

    while True:
        right_grid_item = grid[right_cursor.to_yx_tuple()]

        if right_grid_item == '|':
            right_cursor = right_cursor + DIRECTIONS.RIGHT.value
            continue

        # Wall or existing water
        if right_grid_item == '#':
            break

        # Open space
        if right_grid_item == '.':
            under_right_grid_item = grid[(right_cursor + DIRECTIONS.DOWN.value).to_yx_tuple()]

            if under_right_grid_item in '~#':
                grid[(right_cursor.to_yx_tuple())] = '|'
                right_cursor = right_cursor + DIRECTIONS.RIGHT.value
                continue
            
            elif under_right_grid_item == '.':
                new_cursors.append(right_cursor)
                break
    
    if len(new_cursors) == 0:
        left_x = cursor.x
        while True: 
            left_x -= 1
            if grid[(cursor.y, left_x)] == '#':
                break
            
        right_x = cursor.x
        while True:
            right_x += 1
            if grid[(cursor.y, right_x)] == '#':
                break

        for i in range(left_x + 1, right_x):
            grid[(cursor.y, i)] = '~'

    return new_cursors

queue = Queue()
queue.put(Vector2(500, 1))
while not queue.empty():

    cursor = queue.get()
    while True:
        if cursor.y > ymax:
            break

        if grid[cursor.to_yx_tuple()] in '|~':
            break

        if grid[cursor.to_yx_tuple()] == '.':
            grid[cursor.to_yx_tuple()] = '|'
            # print_grid(grid)

        peek_down = cursor + DIRECTIONS.DOWN.value
        
        if grid[peek_down.to_yx_tuple()] == '.':
            cursor = peek_down
            continue
        
        elif grid[peek_down.to_yx_tuple()] in '~#':
            new_cursors = []
            
            while len(new_cursors) == 0:
                new_cursors = fill_left_right_get_new_cursors(grid, cursor)
                cursor = cursor + DIRECTIONS.UP.value

                if len(new_cursors) == 0 and grid[cursor.to_yx_tuple()] != '|':
                    grid[cursor.to_yx_tuple()] = '|'

                # print_grid(grid)

            for new_cursor in new_cursors:
                queue.put(new_cursor)
            
            # Move onto next cursor
            break

print(sum(1 for coords, val in grid.items() if val in '|~' and coords[0] >= ymin))