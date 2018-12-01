from file_importer import FileImporter

inp = list(map(int, FileImporter.get_input("/../input/1.txt").split("\n")))

freqset = set([0]) 
_sum = 0
i = 0

while True:
    _sum += inp[i]

    if _sum in freqset:
        print(_sum)
        break

    freqset.add(_sum)

    i = (i + 1) % len(inp)

    