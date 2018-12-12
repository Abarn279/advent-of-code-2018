from file_importer import FileImporter
from aoc_utils import Vector2

SERIAL_NUMBER = int(FileImporter.get_input("/../input/11.txt"))

def get_power_level(x, y, serial):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial
    power_level *= rack_id
    hundreds_digit = str(power_level)[:-2][-1]
    return int(hundreds_digit) - 5

grid_size = 301
grid = [[None for i in range(grid_size)] for j in range(grid_size)]

subgrid_sums_by_size = { }
def get_subgrid_total(grid, x, y, s):
    ''' Get the total for a subgrid with topleft corner == x,y and size == s '''

    # Use memoization
    if (x, y, s) in subgrid_sums_by_size:
        return subgrid_sums_by_size[(x, y, s)]

    subgrid_power_level = 0

    # Base case
    if s == 1:
        if grid[y][x] == None:
            grid[y][x] = get_power_level(x, y, SERIAL_NUMBER)
        subgrid_power_level += grid[y][x]

    # Even case - call 4 times for each quadrant
    elif s % 2 == 0:
        half_size = s // 2
        subgrid_power_level += get_subgrid_total(grid, x, y, half_size)
        subgrid_power_level += get_subgrid_total(grid, x + half_size, y, half_size)
        subgrid_power_level += get_subgrid_total(grid, x, y + half_size, half_size) 
        subgrid_power_level += get_subgrid_total(grid, x + half_size, y + half_size, half_size)

    # Odd case - call for the subgrid of size - 1 starting in the top left corner, then for right and bottom edges one by one
    else:
        one_less_size = s - 1
        subgrid_power_level += get_subgrid_total(grid, x, y, one_less_size)
        
        # Add the bottom row
        for xn in range(x, x + s):
            subgrid_power_level += get_subgrid_total(grid, xn, y + s - 1, 1)
        # Add the right column, minus the bottom right corner (already counted above)
        for yn in range(y, y + s - 1):
            subgrid_power_level += get_subgrid_total(grid, x + s - 1, yn, 1)

    subgrid_sums_by_size[(x, y, s)] = subgrid_power_level
    return subgrid_power_level


max_subgrid = 0
max_subgrid_xy = None
max_subgrid_size = 0
# y pairs with j, x pairs with i
for y in range(1, grid_size - 1):
    for x in range(1, grid_size - 1):
        for subgrid_size in range(1, grid_size - max(x, y)):
            subgrid_total = get_subgrid_total(grid, x, y, subgrid_size)

            if subgrid_total > max_subgrid:
                max_subgrid = subgrid_total
                max_subgrid_xy = Vector2(x, y)
                max_subgrid_size = subgrid_size

print(max_subgrid_xy)
print(max_subgrid_size)
