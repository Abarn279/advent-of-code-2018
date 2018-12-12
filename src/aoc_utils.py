class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y)
    def __str__(self):
        return self.__repr__()

def id_gen(start_at):
    while True:
        yield start_at
        start_at += 1
