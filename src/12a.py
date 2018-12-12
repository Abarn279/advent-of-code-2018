from file_importer import FileImporter
import re

def get_generation_start(pots: dict):
    return min(k for k, v in pots.items() if v) - 2

def get_plant_str(pots, center_ind):
    final = ""
    for i in range(center_ind - 2, center_ind + 3):
        if i not in pots or not pots[i]:
            final += '.'
        elif pots[i]:
            final += '#'
    return final 

inp = FileImporter.get_input("/../input/12.txt").split("\n")

initial_state_str = re.match('initial state: (.+)', inp.pop(0)).group(1)
inp.pop(0)

rules = set()
for i in inp:
    [rule, val] = re.match('([\.#]+) => ([\.#])', i).groups()
    if val == '#':
        rules.add(rule)

# Dictionary of position to bool of whether or not plant exists
pots = { }
pots_nextgen = { }
for i in range(len(initial_state_str)):
    pots[i] = True if initial_state_str[i] == '#' else False

for generation in range(20):
    # Start at 2 left from the first plant
    start_ind = get_generation_start(pots)

    # Ensure there's empty entries for 2 indices left of first plant
    if start_ind not in pots: pots[start_ind] = False
    if start_ind + 1 not in pots: pots[start_ind + 1] = False

    for plant_ind in range(start_ind, len(pots) - start_ind):
        pots_nextgen[plant_ind] = True if get_plant_str(pots, plant_ind) in rules else False

    pots = pots_nextgen.copy()
    pots_nextgen = { }
    
print(sum(k for k,v in pots.items() if v))
