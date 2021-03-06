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
        self.infinite = False
    def manhattan_distance(self, x, y):
        return abs(self.x - x) + abs(self.y - y)
    def __str__(self):
        return self.id
    def __repr__(self):
        return self.__str__()

class PointGrid:
    def __init__(self, pt_list):
        self.xmax = max(pt_list, key = lambda point: point.x).x                 
        self.ymax = max(pt_list, key = lambda point: point.y).y
        self.xmin = min(pt_list, key = lambda point: point.x).x
        self.ymin = min(pt_list, key = lambda point: point.y).y
        self.pt_list = pt_list
        self.grid = [['.' for i in range(self.xmax + 1)] for j in range(self.ymax + 1)] 

        for point in self.pt_list:
            self.grid[point.y][point.x] = point

        self.areas = {i.id : 1 for i in self.pt_list}
        
    def fill_nearest(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == '.':
                    nearest_dict = {point.id : point.manhattan_distance(x, y) for point in self.pt_list}
                    nearest_val = min(nearest_dict.values())
                    nearest_keys = [i for i in nearest_dict if nearest_dict[i] == nearest_val]

                    if len(nearest_keys) > 1:
                        continue
                    
                    nearest_key = nearest_keys[0]

                    self.grid[y][x] = nearest_key.lower()
                    
                    if (nearest_key in self.areas):
                        self.areas[nearest_key] += 1

    def get_biggest_area(self):
        for x in range(self.xmin, self.xmax + 1):
            self.areas.pop(str(self.grid[self.ymin][x]).upper(), None)
            self.areas.pop(str(self.grid[self.ymax][x]).upper(), None)

        for y in range(self.ymin, self.ymax + 1):
            self.areas.pop(str(self.grid[y][self.xmin]).upper(), None)
            self.areas.pop(str(self.grid[y][self.xmax]).upper(), None)

        return self.areas[max(self.areas, key = self.areas.get)]

    def __repr__(self):
        ''' View for debugging '''
        st = ""
        for y in self.grid:
            for x in y:
                empty = '  ' if len(str(x)) == 1 else ' '
                st += str(x) + empty
            st += '\n'
        return st

    def __str__(self):
        return self.__repr__()

points = [Point(list(map(int, i.split(', ')))) for i in FileImporter.get_input("/../input/6.txt").split("\n")]

pointgrid = PointGrid(points)
pointgrid.fill_nearest()

print(pointgrid.get_biggest_area())