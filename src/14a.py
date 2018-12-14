from file_importer import FileImporter

n_recipes = int(FileImporter.get_input("/../input/14.txt"))

scoreboard = '37'
elf_1_recipe_i = 0
elf_2_recipe_i = 1

get_new_recipes = lambda a, b: str(int(a) + int(b))

while len(scoreboard) < n_recipes + 10:
    scoreboard += get_new_recipes(scoreboard[elf_1_recipe_i], scoreboard[elf_2_recipe_i])

    elf_1_recipe_i = (elf_1_recipe_i + 1 + int(scoreboard[elf_1_recipe_i])) % len(scoreboard)
    elf_2_recipe_i = (elf_2_recipe_i + 1 + int(scoreboard[elf_2_recipe_i])) % len(scoreboard)

print(scoreboard[-10:])