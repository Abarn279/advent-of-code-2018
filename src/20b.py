from file_importer import FileImporter
from aoc_utils import Vector2

class Location:
    def __init__(self, coords, dist):
        self.coords = coords;self.dist = dist
    def key(self):
        return self.coords.to_tuple()

DIRECTIONS = { 'N': Vector2(0, 1), 'E': Vector2(1, 0), 'S': Vector2(0, -1), 'W': Vector2(-1, 0) }

path_regex = FileImporter.get_input("/../input/20.txt")[1:-1]

loc = Location(Vector2(0, 0), 0)
grid = {loc.key(): loc}
stack = []
for c in path_regex:
    if c in DIRECTIONS:
        loc = Location(loc.coords + DIRECTIONS[c], loc.dist + 1)
        if loc.key() not in grid:
            grid[loc.key()] = loc
    elif c == '(':
        stack.append(loc)
    elif c == ')':
        loc = stack.pop()
    elif c == '|':
        loc = stack[-1]

print(sum(1 for k, v in grid.items() if v.dist >= 1000))


