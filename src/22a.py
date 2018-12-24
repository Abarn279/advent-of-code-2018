from file_importer import FileImporter
from aoc_utils import Vector2

geological_indexes = {}
erosion_levels = {}

inp = FileImporter.get_input("/../input/22.txt").split("\n")

depth = int(inp[0].split(' ')[1].replace(',', ''))
target = Vector2(*list(map(int, inp[1].split(' ')[1].split(','))))

def get_risk_level(coords: Vector2):
    return get_erosion_level(coords) % 3

def get_erosion_level(coords: Vector2):
    '''A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183. Then:

If the erosion level modulo 3 is 0, the region's type is rocky.
If the erosion level modulo 3 is 1, the region's type is wet.
If the erosion level modulo 3 is 2, the region's type is narrow.'''
    global erosion_levels
    global depth

    coord_key = coords.to_tuple()
    if coord_key in erosion_levels:
        return erosion_levels[coord_key]

    erosion_level = (get_geological_index(coords) + depth) % 20183
    erosion_levels[coord_key] = erosion_level
    return erosion_level

def get_geological_index(coords: Vector2):
    ''' The region at 0,0 (the mouth of the cave) has a geologic index of 0.
The region at the coordinates of the target has a geologic index of 0.
If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
Otherwise, the region's geologic index is the result of multiplying the erosion levels of the regions at X-1,Y and X,Y-1. '''
    global geological_indexes
    global target

    coord_key = coords.to_tuple()
    if coord_key in geological_indexes:
        return geological_indexes[coord_key]

    answer = None
    if coords == Vector2(0, 0) or coords == target:
        answer = 0
    elif coords.y == 0:
        answer = coords.x * 16807
    elif coords.x == 0:
        answer = coords.y * 48271
    else:
        answer = get_erosion_level(Vector2(coords.x - 1, coords.y)) * get_erosion_level(Vector2(coords.x, coords.y - 1))

    geological_indexes[coord_key] = answer
    return answer

print(sum(get_risk_level(Vector2(x, y)) for x in range(target.x + 1) for y in range(target.y + 1)))
