from file_importer import FileImporter
import re
from aoc_utils import Vector3

class Nanobot:
    def __init__(self, pos: Vector3, radius):
        self.pos = pos
        self.radius = radius

inp = FileImporter.get_input("/../input/23.txt").split("\n")
nanobots = []
for i in inp:
    x, y, z, r = list(map(int, re.match('pos=<(-*\d+),(-*\d+),(-*\d+)>, r=(\d+)', i).groups()))
    nanobots.append(Nanobot(Vector3(x, y, z), r))

strongest = max(nanobots, key = lambda x: x.radius)

print(sum(1 for i in nanobots if i.pos.manhattan_distance(strongest.pos) <= strongest.radius))
    