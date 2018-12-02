from file_importer import FileImporter
from collections import defaultdict

ids = FileImporter.get_input("/../input/2.txt").split("\n")

twos = 0
threes = 0
for id in ids:
    letter_count = defaultdict(lambda: 0)
    for letter in id:
        letter_count[letter] += 1
    
    if 2 in letter_count.values():
        twos += 1
    if 3 in letter_count.values():
        threes += 1

print(twos * threes)