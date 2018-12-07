from file_importer import FileImporter
import string
import uuid

def get_name():
    names = list(string.ascii_uppercase)
    names += [str(i[0]) + str(i[1]) for i in list(zip(string.ascii_uppercase, string.ascii_uppercase))]
    while True:
        yield names.pop(0)

name_gen = get_name()

class Point:
    def __init__(self, xy_list):
        self.x = xy_list[0];self.y = xy_list[1]
        self.id = next(name_gen)
    def manhattan_distance(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

class PointGrid:
    def __init__(self, pt_list):
        self.xmax = max(pt_list, key = lambda point: point.x).x                 
        self.ymax = max(pt_list, key = lambda point: point.y).y
        self.pt_list = pt_list
        self.grid = [['.' for i in range(self.xmax + 1)] for j in range(self.ymax + 1)] 

        for point in self.pt_list:
            self.grid[point.y][point.x] = point

    def get_region_of_distance_under_limit(self, limit):
        total_under_limit = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                distances = sum(point.manhattan_distance(x, y) for point in self.pt_list)
                if distances < limit:
                    total_under_limit += 1
        return total_under_limit

points = [Point(list(map(int, i.split(', ')))) for i in FileImporter.get_input("/../input/6.txt").split("\n")]

pointgrid = PointGrid(points)
print(pointgrid.get_region_of_distance_under_limit(10000))