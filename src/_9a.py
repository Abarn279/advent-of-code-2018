from file_importer import FileImporter
import re

class Marble:
    def __init__(self, _id, prev = None, nxt = None):
        self._id = _id
        self.prev = prev
        self.nxt = nxt

class MarbleCircle:
    def __init__(self):
        self.current_node = Marble(0)
        self.current_node.nxt = self.current_node
        self.current_node.prev = self.current_node

    def take_turn(self, marble_id):
        ''' Take turn, return the score achieved from this turn '''

        if (marble_id % 23 == 0):
            return marble_id + self.remove_7_counterclockwise()

        new_node = Marble(marble_id)

        # Set the node to the right of new one
        node_to_right = self.current_node.nxt.nxt
        new_node.nxt = node_to_right
        node_to_right.prev = new_node
        
        # Set the node to the left of new one
        node_to_left = self.current_node.nxt
        new_node.prev = node_to_left
        node_to_left.nxt = new_node

        # Set current node to this new one
        self.current_node = new_node

        return 0

    def remove_7_counterclockwise(self):
        for i in range(6):
            self.current_node = self.current_node.prev

        # Delete the node, update the connections        
        to_delete = self.current_node.prev
        val = to_delete._id
        self.current_node.prev = to_delete.prev
        to_delete.prev.nxt = self.current_node
        del to_delete

        return val
        
inp = FileImporter.get_input("/../input/9.txt")
[players, last_marble] = [i for i in re.match('(\d+) players; last marble is worth (\d+) points', inp).groups()]
player_scores = [0 for i in range(int(players))]
circle = MarbleCircle()
curr_player = 0

for marble_id in range(1, int(last_marble) + 1):
    player_scores[curr_player] += circle.take_turn(marble_id)
    curr_player = (curr_player + 1) % len(player_scores) 

print(max(player_scores))
