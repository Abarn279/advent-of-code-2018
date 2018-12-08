from file_importer import FileImporter

def inp_gen():
    inp = list(map(int, FileImporter.get_input("/../input/8.txt").split(' ')))
    while len(inp) > 0:
        yield inp.pop(0)
inp_gen = inp_gen()

class Node:
    def __init__(self, num_child, num_metadata):
        self.children = []
        for i in range(num_child):
            self.children.append(Node(next(inp_gen), next(inp_gen)))

        self.metadata_entries = []
        for i in range(num_metadata):
            self.metadata_entries.append(next(inp_gen))

    def sum_metadata(self):
        return sum(self.metadata_entries) + sum(i.sum_metadata() for i in self.children)

root = Node(next(inp_gen), next(inp_gen))
print(root.sum_metadata())