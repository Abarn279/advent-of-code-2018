from file_importer import FileImporter
from aoc_utils import Vector2

serial_number = int(FileImporter.get_input("/../input/11.txt"))

def get_power_level(x, y, serial):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial
    power_level *= rack_id
    hundreds_digit = str(power_level)[:-2][-1]
    return int(hundreds_digit) - 5

grid_size = 301
subgrid_size = 3
grid = [[None for i in range(grid_size)] for j in range(grid_size)]

max_subgrid = 0
max_subgrid_xy = None
# y pairs with j, x pairs with i
for y in range(1, grid_size - 3):
    for x in range(1, grid_size - 3):
        subgrid_total = 0
        for j in range(0, subgrid_size):
            for i in range(0, subgrid_size):
                if grid[y+j][x+i] == None:
                    grid[y+j][x+i] = get_power_level(x+i, y+j, serial_number)
                subgrid_total += grid[y+j][x+i]

        if subgrid_total > max_subgrid:
            max_subgrid = subgrid_total
            max_subgrid_xy = Vector2(x, y)

print(max_subgrid_xy)
