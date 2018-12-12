from file_importer import FileImporter
import re

def get_generation_start_end(pots: dict):
    return (min(k for k, v in pots.items() if v) - 2, max(k for k, v in pots.items() if v) + 2)

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

total_plants = 0
last_sum = 0

# Math for repeating
generation_starts_repeating = 0

for generation in range(10000):
    # Start at 2 left from the first plant
    min_ind, max_ind = get_generation_start_end(pots)

    # Ensure there's empty entries for 2 indices left of first plant
    if min_ind not in pots: pots[min_ind] = False
    if min_ind + 1 not in pots: pots[min_ind + 1] = False
    if max_ind not in pots: pots[max_ind] = False
    if max_ind + 1 not in pots: pots[max_ind - 1] = False

    for plant_ind in range(min_ind, max_ind + 1):
        pots_nextgen[plant_ind] = True if get_plant_str(pots, plant_ind) in rules else False

    # Do pot stuff
    pots = pots_nextgen.copy()
    pots_nextgen = { }

    # This is all new. I started by printing out the change in sum over time, and once you reach a few thousand iterations, the change in sum
    # hits a constant number. Programatically finding when it changed, and simulating that change over the rest of the (50b - already_simulated) generations.
    _sum = sum(k for k,v in pots.items() if v)
    sum_dif = _sum - last_sum

    # Found through iterating on my input
    if sum_dif == 58:
        generation_starts_repeating = generation
        total_plants = _sum
        break

    last_sum = _sum
    
print(total_plants + (50000000000 - (generation_starts_repeating + 1)) * 58)