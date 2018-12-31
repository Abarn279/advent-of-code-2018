from file_importer import FileImporter
from aoc_utils import Vector4
from uuid import uuid1

class Constellation:
    def __init__(self, initial):
        self.points = [initial] 
        self.id = uuid1()

    def can_join(self, point_to_join: Vector4):
        for point in self.points:
            if point.manhattan_distance(point_to_join) <= 3:
                return True
        return False

    def merge(self, other):
        for point in other.points:
            self.points.append(point)

    def __hash__(self):
        return hash(str(self.id))

points = [Vector4(*list(map(int, i.split(',')))) for i in FileImporter.get_input("/../input/25.txt").split("\n")]

constellations = set()
for point in points:
    nearby = []
    for constellation in constellations: 
        if constellation.can_join(point):
            nearby.append(constellation)

    if len(nearby) > 1:
        old_const = set(nearby[1:])
        for old in old_const:
            nearby[0].merge(old)
        nearby[0].points.append(point)

        constellations = set(i for i in constellations if i not in old_const)

    elif len(nearby) == 1:
        nearby[0].points.append(point)

    else:
        constellations.add(Constellation(point))
    
print(len(constellations))
