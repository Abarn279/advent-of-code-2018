###################
#
# Note - this is a visual program. Upon running, it will pull up a canvas that cycles through the point updates, creating a visual of letters.
#
###################

from file_importer import FileImporter
from time import sleep
from tkinter import Canvas, mainloop, Tk
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

# Setup gui and canvas
gui = Tk()
c_height = 1000
c_width = 1000
canvas = Canvas(gui, width=1000, height=1000)
canvas.pack()

# Get points
to_point = lambda inp_ary: Point(Vector2(int(inp_ary[0]), int(inp_ary[1])), Vector2(int(inp_ary[2]), int(inp_ary[3])))
points = [to_point(re.match('position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>', i).groups()) for i in FileImporter.get_input("/../input/10.txt").split("\n")]

# Size of each grid item
point_size = 5

# Offset the "camera" for viewing. Found via testing
offset = -50

# Get a point for the canvas (scaled and offset)
get_canvas_point = lambda vec2: Vector2((vec2.pos.x * point_size) + (offset * point_size), (vec2.pos.y * point_size) + (offset * point_size))

def draw_grid():
    for x in range(0, c_width, point_size):
        canvas.create_line(x, 0, x, c_height)
    for y in range(0, c_height, point_size):
        canvas.create_line(0, y, c_width, y)

for update in range(50000):
    drawing = False

    if max(points, key = lambda point: point.pos.x).pos.x - min(points, key = lambda point: point.pos.x).pos.x < 200:
        drawing = True

    for point in points:
        point.update()

        if drawing:
            top_left_coords = get_canvas_point(point)
            canvas.create_rectangle(top_left_coords.x, top_left_coords.y, top_left_coords.x + point_size, top_left_coords.y + point_size, fill = "#000000")
    
    if drawing:
        draw_grid()
        gui.update()
        sleep(.35)
        canvas.delete('all')

mainloop()
