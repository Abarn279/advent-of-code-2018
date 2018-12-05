from file_importer import FileImporter
import string
import sys

polymer = FileImporter.get_input("/../input/5.txt")

is_opp_polar = lambda a, b: ord(a) - 32 == ord(b) or ord(a) + 32 == ord(b)

def react_polymer(polymer): 
    i = 0
    while i < len(polymer) - 1: 
        if is_opp_polar(polymer[i], polymer[i+1]):
            polymer = polymer[:i] + polymer[i+2:]
            i = max(0, i - 1)
            continue
        i += 1
    return polymer

shortest_length = sys.maxsize
for c in string.ascii_lowercase:
    new_polymer = "".join(x for x in polymer if x not in [c, chr(ord(c) - 32)])
    reacted = react_polymer(new_polymer)
    if len(reacted) < shortest_length:
        shortest_length = len(reacted)

print(shortest_length)
