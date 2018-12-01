from file_importer import FileImporter
import itertools

inp = list(map(int, FileImporter.get_input("/../input/1.txt").split("\n")))

freqset = set([0]) 
_sum = 0

for i in itertools.cycle(inp):
    _sum += i

    if _sum in freqset:
        print(_sum)
        break

    freqset.add(_sum)
   