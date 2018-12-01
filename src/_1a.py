from file_importer import FileImporter

inp = FileImporter.get_input("/../input/1.txt").split("\n")

print(sum(int(i) for i in inp))