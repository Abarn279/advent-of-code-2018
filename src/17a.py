from file_importer import FileImporter
from aoc_utils import Vector2
from collections import defaultdict
from enum import Enum
import re

# Directional vectors in grid
#              0              1              2              3
#              UP             RIGHT          DOWN           LEFT
DIRECTIONS = [Vector2(0, -1), Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0)]

def print_grid(grid):
    for y in range(0, 14):
        for x in range(494, 508):
            print(grid[(y, x)], end="")
        print()

class StreamWriter:
    def __init__(self, grid, direction_ind, start_pos: Vector2, parent = None):
        self.direction_ind = direction_ind
        self.current_pos = start_pos

        self.children = []
        self.parent = parent

        self.complete = False
        self.is_dead_end = False
    
    def tick(self):
        if len(self.children) > 0:
            # Tick all children
            for child in self.children:
                child.tick()
        
        # If we're at an open spot, fill it with water.
        if self.grid[self.current_pos.to_yx_tuple()] == '.':
            self.grid[self.current_pos.to_yx_tuple()] = '|'

            # If we're moving right/left, check down. If empty, create a new one and stop this one.
            if self.direction_ind in [1, 3]:
                
                pos_below = self.current_pos + DIRECTIONS[2]
                if self.grid[pos_below.to_yx_tuple()] == '.':
                    self.complete = True
                    new_stream = StreamWriter(self.grid, 2, pos_below, self)
                    self.children.append(new_stream)
                    return
        
        elif self.grid[self.current_pos.to_yx_tuple()] == '#':


            





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

print_grid(grid)