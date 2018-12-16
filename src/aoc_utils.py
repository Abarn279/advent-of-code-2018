class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def add(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    def __add__(self, other):
        return self.add(other)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash(f'{self.x},{self.y}')
    def __repr__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y)
    def __str__(self):
        return self.__repr__()

def id_gen(start_at):
    while True:
        yield start_at
        start_at += 1
