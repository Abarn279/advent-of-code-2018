import heapq
from aoc_utils import Vector2

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def astar(start, is_goal_fn, heuristic_fn, cost_fn, get_neighbors_fn, get_key_fn):
    queue = PriorityQueue()
    queue.put(start, 0)
    visited = set()
    
    last_node = dict()
    cost_from_start = dict()

    last_node[get_key_fn(start)] = None
    cost_from_start[get_key_fn(start)] = 0

    while not queue.empty():
        current = queue.get()

        if is_goal_fn(current):
            break 

        for neighbor in get_neighbors_fn(current):
            new_cost = cost_from_start[get_key_fn(current)] + cost_fn(current, neighbor)
            if get_key_fn(neighbor) not in cost_from_start or new_cost < cost_from_start[get_key_fn(neighbor)]:
                cost_from_start[get_key_fn(neighbor)] = new_cost
                priority = new_cost + heuristic_fn(neighbor)
                queue.put(neighbor, priority)
                last_node[get_key_fn(neighbor)] = current

    return cost_from_start[get_key_fn(current)]