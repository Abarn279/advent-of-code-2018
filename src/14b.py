from file_importer import FileImporter

n_recipes = "607331" #FileImporter.get_input("/../input/14.txt")

scoreboard = ['3', '7']
elf_1_recipe_i = 0
elf_2_recipe_i = 1

get_new_recipes = lambda a, b: list(str(int(a) + int(b)))

len_last_chars = len(n_recipes)
while scoreboard[-len_last_chars:] != list(str(n_recipes)):
    scoreboard += get_new_recipes(scoreboard[elf_1_recipe_i], scoreboard[elf_2_recipe_i])

    elf_1_recipe_i = (elf_1_recipe_i + 1 + int(scoreboard[elf_1_recipe_i])) % len(scoreboard)
    elf_2_recipe_i = (elf_2_recipe_i + 1 + int(scoreboard[elf_2_recipe_i])) % len(scoreboard)

print(len(scoreboard) - len_last_chars)