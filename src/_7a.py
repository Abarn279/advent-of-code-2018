from file_importer import FileImporter
from queue import Queue

class Node:
    def __init__(self, id):
        self.id = id
        self.requirements_before = []
        self.available_after = []
        self.completed = False
    def add_requirement(self, node):
        self.requirements_before.append(node)
        node.available_after.append(self)
    def __repr__(self):
        return self.id

def get_node_set(inp):
    ''' Get the set of all nodes from the input list '''
    nodes = { }
    for requirement in inp:
        first, second = requirement[1], requirement[7]

        if first not in nodes: 
            nodes[first] = Node(first)

        if second not in nodes: 
            nodes[second] = Node(second)

        nodes[second].add_requirement(nodes[first])

    return set(nodes.values())

def get_root_nodes(node_set):
    ''' Get the list of nodes that have no requirements to get started '''
    roots = []
    for node in node_set:
        if len(node.requirements_before) == 0:
            roots.append(node)
    return roots

def get_order(root_list):
    ''' Get the string order of node execution '''
    final_order = ""

    available_nodes = root_list[:]

    # Effectively a BFS where we sort the queue every time
    while len(available_nodes) > 0:
        available_nodes = sorted(available_nodes, key = lambda x: x.id)

        first_all_completed = None
        for i in range(len(available_nodes)):
            if all(i.completed for i in available_nodes[i].requirements_before):
                first_all_completed = i
                break

        n = available_nodes.pop(first_all_completed)
        final_order += n.id
        n.completed = True

        n.available_after = sorted(n.available_after, key = lambda x: x.id)     # Sort the edge list alphabetically, queue those nodes
        for connected_n in n.available_after:
            if not connected_n.completed and connected_n not in available_nodes:
                available_nodes.append(connected_n)
    
    return final_order

inp = [i.split(' ') for i in FileImporter.get_input("/../input/7.txt").split("\n")]
nodes = get_node_set(inp)
root_nodes = get_root_nodes(nodes)
print(get_order(root_nodes))