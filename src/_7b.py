from file_importer import FileImporter
from queue import Queue
import string

class Node:
    def __init__(self, id):
        self.id = id
        self.requirements_before = []
        self.available_after = []
        self.completed = False
    def add_requirement(self, node):
        self.requirements_before.append(node)
        node.available_after.append(self)
    def get_time_requirement(self):
        return 60 + string.ascii_uppercase.index(self.id) + 1
    def __repr__(self):
        return self.id

class Worker:
    def __init__(self):
        self.time_remaining_on_current = 0
        self.current_node = None
    def give_new_node(self, node):
        self.current_node = node
        self.time_remaining_on_current = node.get_time_requirement()
    def update(self):
        ''' Update this timestep, return the node if completed else nothing '''
        self.time_remaining_on_current -= 1
        if self.time_remaining_on_current == 0:
            self.current_node.completed = True
            return self.current_node
        else:
            return None
    def is_done(self):
        return self.time_remaining_on_current <= 0

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

def get_execution_time(root_list, num_workers):
    ''' Get the string order of node execution '''
    workers = [Worker() for i in range(num_workers)]

    update_count = 0                                                            # This will be the final answer
    available_nodes = root_list[:]

    while not all(worker.is_done() for worker in workers) or len(available_nodes) > 0:
        available_nodes = sorted(available_nodes, key = lambda x: x.id)

        for worker in filter(lambda worker: worker.is_done(), workers):         # If a worker is done, try and give him a new task

            first_all_completed = None                                          # Give them the first alphabetical task that has all prerequisites completed
            for i in range(len(available_nodes)):
                if all(i.completed for i in available_nodes[i].requirements_before):
                    first_all_completed = i
                    break

            if first_all_completed is not None:
                worker.give_new_node(available_nodes.pop(first_all_completed))
            else:
                break

        update_count += 1                                                       # Run updates on workers
        for worker in workers:
            completed_node = worker.update()                                    # Update will return the completed node if the worker is done

            if completed_node is not None:
                completed_node.available_after = sorted(completed_node.available_after, key = lambda x: x.id)     # Sort the edge list alphabetically, queue those nodes

                for connected_n in completed_node.available_after:
                    if not connected_n.completed and connected_n not in available_nodes:
                        available_nodes.append(connected_n)

    return update_count

        
    

inp = [i.split(' ') for i in FileImporter.get_input("/../input/7.txt").split("\n")]
nodes = get_node_set(inp)
root_nodes = get_root_nodes(nodes)
print(get_execution_time(root_nodes, 5))