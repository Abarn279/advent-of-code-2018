from file_importer import FileImporter
from aoc_utils import Vector2
from collections import defaultdict
from enum import Enum
from queue import Queue
import re

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

# Put the spout
grid[(0, 500)] = '+'

ymax = max(grid.keys(), key = lambda x: x[0])[0]
ymin = min(grid.keys(), key = lambda x: x[0])[0]
xmax = max(grid.keys(), key = lambda x: x[1])[1]
xmin = min(grid.keys(), key = lambda x: x[1])[1]

def print_grid(grid):
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            print(grid[(y, x)], end="")
        print()

def fill_left_right_get_new_cursors(grid, cursor): 
    ''' Fill the spaces to the left/right, return an array of new cursors '''
    left_cursor = cursor + DIRECTIONS.LEFT
    right_cursor = cursor + DIRECTIONS.RIGHT
    new_cursors = []
    while True:
        left_grid_item = grid[left_cursor.to_yx_tuple()]

        # Wall
        if left_grid_item == '#':
            break

        # Open space
        if left_grid_item == '.':
            under_left_grid_item = grid[(left_cursor + DIRECTIONS.DOWN).to_yx_tuple()]

            if under_left_grid_item == '~':
                left_cursor = left_cursor + DIRECTIONS.LEFT
                grid[(left_cursor.to_yx_tuple())] = '|'
                continue
            
            elif under_left_grid_item == '.':
                new_cursors.append(left_cursor + DIRECTIONS.LEFT)
                break

    while True:
        right_grid_item = grid[right_cursor.to_yx_tuple()]

        # Wall
        if right_grid_item == '#':
            break

        # Open space
        if right_grid_item == '.':
            under_right_grid_item = grid[(right_cursor + DIRECTIONS.DOWN).to_yx_tuple()]

            if under_right_grid_item == '~':
                right_cursor = right_cursor + DIRECTIONS.RIGHT
                grid[(right_cursor.to_yx_tuple())] = '|'
                continue
            
            elif under_right_grid_item == '.':
                new_cursors.append(right_cursor + DIRECTIONS.RIGHT)
                break
    
    return new_cursors
    
print_grid(grid)

queue = Queue()
queue.put(Vector2(500, 0))
while not queue.empty():

    cursor = queue.get()
    while True:
        if grid[cursor.to_yx_tuple()] == '.':
            grid[cursor.to_yx_tuple()] == '|'

        peek_down = cursor + DIRECTIONS.DOWN
        
        if grid[peek_down.to_yx_tuple()] == '.':
            cursor = peek_down
            continue
        
        elif grid[peek_down.to_yx_tuple()] == '#':
            new_cursors = []
            
            while len(new_cursors) == 0:
                new_cursors = fill_left_right_get_new_cursors(grid, cursor)
                cursor = cursor + DIRECTIONS.UP

            for new_cursor in new_cursors:
                queue.put(new_cursor)

            
print_grid(grid)