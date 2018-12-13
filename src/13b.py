from file_importer import FileImporter
from aoc_utils import Vector2
import uuid

# Directional vectors in grid
#              0        1       2       3
#              UP       RIGHT   DOWN    LEFT
DIRECTIONS = [Vector2(0, -1), Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0)]
ARROW_TO_DIRECTION = { '^' : 0, '>' : 1, 'v' : 2, '<' : 3 }
ARROW_TO_GRID_UNDER = { '^' : '|', '>' : '-', 'v' : '|', '<' : '-' }

class Cart:
    def __init__(self, position: Vector2, direction_ind: int):
        self.position = position
        self.direction_ind = direction_ind
        self.id = uuid.uuid1()

        # Left turn = 0, Straight = 1, Right turn = 2
        self.intersection_turn = 2

    def turn(self, grid):
        # Corners
        if grid[self.position.y][self.position.x] == '/':
            if self.direction_ind in [0, 2]:
                self.direction_ind += 1
            else:
                self.direction_ind = (self.direction_ind - 1) % 4

        elif grid[self.position.y][self.position.x] == '\\':
            if self.direction_ind in [0, 2]:
                self.direction_ind = (self.direction_ind - 1) % 4
            else:
                self.direction_ind = (self.direction_ind + 1) % 4
        
        # Intersection
        elif grid[self.position.y][self.position.x] == '+':
            self.intersection_turn = (self.intersection_turn + 1) % 3

            if self.intersection_turn == 0:
                self.direction_ind = (self.direction_ind - 1) % 4
            elif self.intersection_turn == 1:
                pass
            elif self.intersection_turn == 2:
                self.direction_ind = (self.direction_ind + 1) % 4

    def tick(self, grid, other_carts):
        ''' Tick. return a tuple of the two colliding objects if theres a collision '''
        self.turn(grid)
        self.position = self.position + DIRECTIONS[self.direction_ind]
        for other_cart in other_carts:
            if other_cart.position == self.position:
                return (self, other_cart)
        return None

def sort_carts(carts):
    carts = sorted(carts, key = lambda x: x.position.y)
    return sorted(carts, key = lambda x: x.position.x)

def get_final_cart_position(grid, carts):
    sorted_carts = carts[:]
    while True:
        sorted_carts = sort_carts(sorted_carts)
        to_remove_ids = []
        for cart in sorted_carts:
            other_carts = [i for i in sorted_carts if i.id != cart.id]

            colliding_carts = cart.tick(grid, other_carts)

            if colliding_carts is not None:
                to_remove_ids = to_remove_ids + [i.id for i in colliding_carts]

        sorted_carts = [i for i in sorted_carts if i.id not in to_remove_ids]

        if len(sorted_carts) == 1:
            return sorted_carts[0].position

grid = [list(i) for i in FileImporter.get_input("/../input/13.txt").split("\n")]
carts = []

# Replace carts with track, create cart objects
for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x] in '^<>v':
            new_cart = Cart(Vector2(x, y), ARROW_TO_DIRECTION[grid[y][x]])
            carts.append(new_cart)
            grid[y][x] = ARROW_TO_GRID_UNDER[grid[y][x]]

print(get_final_cart_position(grid, carts))
