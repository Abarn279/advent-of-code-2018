from file_importer import FileImporter

polymer = FileImporter.get_input("/../input/5.txt")

def is_opp_polar(a, b): 
    return ord(a) - 32 == ord(b) or ord(a) + 32 == ord(b)

i = 0
while i < len(polymer) - 1: 
    if is_opp_polar(polymer[i], polymer[i+1]):
        polymer = polymer[:i] + polymer[i+2:]
        i = max(0, i - 1)
        continue

    i += 1

print(len(polymer))