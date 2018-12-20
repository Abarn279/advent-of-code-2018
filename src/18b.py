from file_importer import FileImporter
from collections import defaultdict
from aoc_utils import Vector2

GRID_SIZE = 0
MINUTES = 10000000

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
last_multiplication = 0

minute_repeat_start = 0         # The minute count that I"m using for repeating
minute_repeat_end = 0
rv_start_repeating = 0          # The resource value at that minute

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

    rv = get_resource_value(grid)
    dif = last_multiplication - rv 
    last_multiplication = rv

    if minute == 551:       # Magic. JK, found this by picking a point in the repitition cycle 
        print(rv)           # (Found this by printing the difference in resource value each time)
                            # and then finding a minute that it all starts repeating. The number i picked is 532 (the 532nd minute).
                            # (1000000000 - 532) % 28 is your final answer, subtract one to get the index. 28 is the amount of minutes it takes to cycle.

    # if dif == -3:           # Found this by testing. This is the number at which it starts to repeat.
    #     if minute_repeat_start == 0:
    #         minute_repeat_start = minute

    #     else:
    #         minute_repeat_end = minute
    #         break

    #     rv_start_repeating = rv

# print(minute_repeat_start)
# print(minute_repeat_end)
# print(minute_repeat_start - minute_repeat_end)

# mod = (1000000000 - 532) % 28