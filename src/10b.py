from file_importer import FileImporter
import re

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y)

class Point:
    def __init__(self, pos: Vector2, vel: Vector2):
        self.pos = pos
        self.vel = vel
    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
    def rev_update(self):
        self.pos.x -= self.vel.x
        self.pos.y -= self.vel.y

# Get points
to_point = lambda inp_ary: Point(Vector2(int(inp_ary[0]), int(inp_ary[1])), Vector2(int(inp_ary[2]), int(inp_ary[3])))
points = [to_point(re.match('position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>', i).groups()) for i in FileImporter.get_input("/../input/10.txt").split("\n")]

updates = 0
current_min = 10000000
while True:
    for point in points:
        point.update()

    updates += 1
    new_min = max(points, key = lambda point: point.pos.x).pos.x - min(points, key = lambda point: point.pos.x).pos.x
    if new_min > current_min:
        updates -= 1
        break
    else:
        current_min = new_min

print(updates)
