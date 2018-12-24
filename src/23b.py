from file_importer import FileImporter
import re
from aoc_utils import Vector3

class Nanobot:
    def __init__(self, pos: Vector3, radius):
        self.pos = pos
        self.radius = radius
    
    def __floordiv__(self, amt):
        return Nanobot(Vector3(self.pos.x // amt, self.pos.y // amt, self.pos.z // amt), self.radius // amt)

inp = FileImporter.get_input("/../input/23.txt").split("\n")
nanobots = []
for i in inp:
    x, y, z, r = list(map(int, re.match('pos=<(-*\d+),(-*\d+),(-*\d+)>, r=(\d+)', i).groups()))
    nanobots.append(Nanobot(Vector3(x, y, z), r))

max_in_range = -1
max_in_range_coords = []

minx, maxx = min(nanobots, key = lambda x: x.pos.x).pos.x, max(nanobots, key = lambda x: x.pos.x).pos.x
miny, maxy = min(nanobots, key = lambda x: x.pos.y).pos.y, max(nanobots, key = lambda x: x.pos.y).pos.y
minz, maxz = min(nanobots, key = lambda x: x.pos.z).pos.z, max(nanobots, key = lambda x: x.pos.z).pos.z
div = 10000000
while True:
    for x in range(minx, maxx + 1, div):
        for y in range(miny, maxy + 1, div):
            for z in range(minz, maxz, div):
                current_pos = Vector3(x, y, z)
                nbs = [nanobot // div for nanobot in nanobots]
                num_in_range = sum(1 for i in nanobots if i.pos.manhattan_distance(current_pos) <= i.radius)
                
                if num_in_range > max_in_range:
                    max_in_range_coords = [current_pos]
                    max_in_range = num_in_range

                elif num_in_range == max_in_range:
                    max_in_range_coords.append(current_pos)

    if div == 1:
        print(min([i.manhattan_distance(Vector3(0,0,0)) for i in max_in_range_coords]))
        break

    else:
        shortest_distance_coord = min(max_in_range_coords, key = lambda x: x.manhattan_distance(Vector3(0,0,0)))
        minx, maxx = shortest_distance_coord.x - div, shortest_distance_coord.x + div
        miny, maxy = shortest_distance_coord.y - div, shortest_distance_coord.y + div
        minz, maxz = shortest_distance_coord.z - div, shortest_distance_coord.z + div
        div //= 10

        