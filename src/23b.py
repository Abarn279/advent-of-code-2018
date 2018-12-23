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

max_in_range = -1
max_in_range_coords = []

for x in range(min(nanobots, key = lambda x: x.pos.x).pos.x, max(nanobots, key = lambda x: x.pos.x).pos.x + 1):
    for y in range(min(nanobots, key = lambda x: x.pos.y).pos.y, max(nanobots, key = lambda x: x.pos.y).pos.y + 1):
        for z in range(min(nanobots, key = lambda x: x.pos.z).pos.z, max(nanobots, key = lambda x: x.pos.z).pos.z + 1):
            current_pos = Vector3(x, y, z)
            num_in_range = sum(1 for i in nanobots if i.pos.manhattan_distance(current_pos) <= i.radius)
            
            if num_in_range > max_in_range:
                max_in_range_coords = [current_pos]
                max_in_range = num_in_range

            elif num_in_range == max_in_range:
                max_in_range_coords.append(current_pos)

print(min(i.manhattan_distance(Vector3(0, 0, 0)) for i in max_in_range_coords))
