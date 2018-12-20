from file_importer import FileImporter
from collections import defaultdict
from aoc_utils import Vector2

GRID_SIZE = 0
MINUTES = 10

def get_surrounding_plots(grid, center_point: Vector2):
    global GRID_SIZE
    plots = []
    for y in range(center_point.y - 1, center_point.y + 2):
        for x in range(center_point.x - 1, center_point.x + 2):
            if y < 0 or y >= GRID_SIZE or x < 0 or x >= GRID_SIZE or Vector2(x, y) == center_point:
                continue
            plots.append(grid[y][x])
    return plots

def get_resource_value(grid):
    tree_sum = sum([sum(1 for i in row if i == '|') for row in grid])
    lumber_sum = sum([sum(1 for i in row if i == '#') for row in grid])
    return tree_sum * lumber_sum


grid = [list(i) for i in FileImporter.get_input("/../input/18.txt").split("\n")]
GRID_SIZE = len(grid)

for minute in range(MINUTES):
    new_grid = [[None for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            surrounding = get_surrounding_plots(grid, Vector2(x, y))
            if grid[y][x] == '.':           # OPEN
                new_grid[y][x] = '|' if surrounding.count('|') >= 3 else '.'

            elif grid[y][x] == '|':         # TREES
                new_grid[y][x] = '#' if surrounding.count('#') >= 3 else '|'

            elif grid[y][x] == '#':         # LUMBERYARD
                new_grid[y][x] = '.' if not (surrounding.count('#') >= 1 and surrounding.count('|')) else '#'

    grid = new_grid[:]

print(get_resource_value(grid))