from file_importer import FileImporter
from aoc_utils import Vector2
from collections import defaultdict

def print_grid(grid):
    ymax = max(grid, key = lambda x: x[1])[1]
    ymin = min(grid, key = lambda x: x[1])[1]
    xmax = max(grid, key = lambda x: x[0])[0]
    xmin = min(grid, key = lambda x: x[0])[0]
    for y in range(ymax, ymin - 1, -1):
        for x in range(xmin, xmax + 1):
            if x == 0 and y == 0:
                print('X', end="")
            elif abs(y + x) % 2 != 0 and grid[(x, y)] == ' ':
                print('?', end="")
            elif y % 2 != 0 and x % 2 != 0:
                print('#', end="")
            else:
                print(grid[(x, y)], end="")
        print()

DIRECTIONS = { 'N': Vector2(0, 1), 'E': Vector2(1, 0), 'S': Vector2(0, -1), 'W': Vector2(-1, 0) }

def get_paths(path_str: str):
    strs = [] 
    
    # First, get the string before the parens.
    before_paren = ""
    while path_str != "":
        to_add = path_str[0]

        if to_add == '(':
            break

        else:
            before_paren += to_add

        path_str = path_str[1:]

    strs += before_paren.split('|')

    if len(path_str) == 0:
        return strs

    # Get the string within the first set of parens. This might include more parens which are recursively called later
    paren_group = ""
    paren_count = 1
    path_str = path_str[1:]
    while True:
        if path_str[0] == '(': paren_count += 1
        elif path_str[0] == ')': 
            paren_count -= 1
            if paren_count == 0:
                path_str = path_str[1:]
                break
        paren_group += path_str[0]
        path_str = path_str[1:]

    # Recursively call for the string within the parens, add any branch onto the last entry of strings created above.
    new_strings = strs[:-1]
    direction_strings = get_paths(paren_group)
    for new in direction_strings:
        new_strings.append(strs[-1] + new)

    if path_str == "":
        return new_strings
    
    # For all of existing branches, add on the string that's after the paren group (recursive)
    final_strings = []
    for old in new_strings:
        for new in get_paths(path_str):
            final_strings.append(old + new)

    return final_strings

def do_path(grid: defaultdict, path_str: str, current_pos: Vector2):
    for direction in path_str:

        door_pos = current_pos + DIRECTIONS[direction]
        next_room_pos = current_pos + (DIRECTIONS[direction] * 2)

        if direction in ['N', 'S']:
            grid[door_pos.to_tuple()] = '-'
        else:
            grid[door_pos.to_tuple()] = '|'

        current_pos = next_room_pos
        grid[current_pos.to_tuple()] = '.'

        for val in DIRECTIONS.values():
            potential_door_position = current_pos + val
            if grid[potential_door_position.to_tuple()] not in ['|', '-']:
                grid[potential_door_position.to_tuple()] = '?'


path_regex = FileImporter.get_input("/../input/20.txt")[1:-1]
grid = defaultdict(lambda: ' ')

grid[(0, 0)] = '.'
for val in DIRECTIONS.values():
    grid[val.to_tuple()] = '?'

paths = get_paths(path_regex)
for path in paths:
    do_path(grid, path, Vector2(0, 0))

# At this point, search through and pathfind

# print_grid(grid)
