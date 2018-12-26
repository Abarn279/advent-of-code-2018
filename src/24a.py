from file_importer import FileImporter
from math import ceil
import re

class Group:
    def __init__(self, num_units: int, hp: int, immunities: list, weaknesses: list, typ: str, ad: int, initiative: int):
        self.max_units = num_units
        self.hp_per_unit = hp
        self.combined_hp = hp * self.max_units
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.type = typ
        self.ad = ad
        self.initiative = initiative

        self.target = None
        self.targeted_by = None

    def get_current_units(self):
        return self.combined_hp // self.hp_per_unit

    def get_effective_power(self):
        return self.get_current_units() * self.ad

    def damage_would_take_from(self, attacker):
        if attacker.type in self.immunities:
            return 0
        
        dmg = attacker.get_effective_power()

        if attacker.type in self.weaknesses:
            dmg *= 2
        
        return dmg

    def take_damage(self, amt):
        real_dmg = amt // self.hp_per_unit * self.hp_per_unit
        self.combined_hp -= real_dmg
        return self.combined_hp <= 0
            
    def do_target_selection(self, enemy_team):
        avail_units = [i for i in enemy_team if i.targeted_by == None and i.damage_would_take_from(self) > 0]
        if len(avail_units) == 0:
            return
        avail_units = sorted(avail_units, key = lambda x: (x.damage_would_take_from(self), x.get_effective_power(), x.initiative), reverse = True)
        self.target = avail_units[0]
        avail_units[0].targeted_by = self

    def is_dead(self):
        return self.combined_hp <= 0

    def __repr__(self):
        return f'{self.id} with {self.get_current_units()} units'

class Team:
    def __init__(self, groups):
        self.groups = groups

    def is_all_dead(self):
        return all(i.is_dead() for i in self.groups)

    def do_target_selection(self, enemy_team):
        groups = sorted(self.groups, key = lambda x: (x.get_effective_power(), x.initiative), reverse = True)

        for group in groups:
            group.do_target_selection(enemy_team.groups)

    def unset_targets(self):
        for i in self.groups:
            i.target = None
            i.targeted_by = None

    def get_total_units(self):
        return sum(i.get_current_units() for i in self.groups)

    def clean_dead(self):
        self.groups = [i for i in self.groups if not i.is_dead()]

class GameManager:
    def __init__(self, team1, team2):
        self.immune_system = team1
        self.infection = team2

    def __do_target_selection(self):
        self.immune_system.do_target_selection(self.infection)
        self.infection.do_target_selection(self.immune_system)

    def __do_attack(self):
        all_groups = self.immune_system.groups + self.infection.groups
        all_groups = sorted(all_groups, key = lambda x: x.initiative, reverse = True)

        for group in all_groups:
            if group.is_dead() or group.target == None: 
                continue
            
            group.target.take_damage(group.target.damage_would_take_from(group))

    def __clean(self):
        self.immune_system.unset_targets()
        self.infection.unset_targets()
        self.immune_system.clean_dead()
        self.infection.clean_dead()

    def do_fight(self):
        self.__do_target_selection()
        self.__do_attack()
        self.__clean()

    def game_over(self):
        return self.immune_system.is_all_dead() or self.infection.is_all_dead()

    def get_winning_army_units(self):
        return max(self.immune_system.get_total_units(), self.infection.get_total_units())

imm_inp, inf_inp = FileImporter.get_input("/../input/24.txt").split("\n\n")
imm_inp = imm_inp.split('\n');imm_inp.pop(0)
inf_inp = inf_inp.split('\n');inf_inp.pop(0)

immune_system_lst = []
infection_lst = []

def get_group(inp_str):
    units, hp, types_str, ad, typ, initiative = re.match('(\d+) units each with (\d+) hit points (\([^)]*\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)', i.replace('\n', '')).groups()

    immunes_lst = []    
    weak_list = []

    if types_str != None:
        types_str = types_str[1:-2]
        types_lst = types_str.split('; ')

        for t in types_lst:
            if t.startswith('weak'):
                c_list = weak_list
            else:
                c_list = immunes_lst
            
            n_t = "".join(t.split(' ')[2:])
            c_list += n_t.split(',')

    return Group(int(units), int(hp), immunes_lst, weak_list, typ, int(ad), int(initiative))

for i in imm_inp:
    immune_system_lst.append(get_group(i))

for i in inf_inp:
    infection_lst.append(get_group(i))

gm = GameManager(Team(immune_system_lst), Team(infection_lst))

while not gm.game_over():
    gm.do_fight()

print(gm.get_winning_army_units())