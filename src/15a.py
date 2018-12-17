from file_importer import FileImporter
from enum import Enum
from aoc_utils import Vector2
from queue import Queue
import uuid

class Team(Enum):
    ELVES = 1,
    GOBLINS = 2

class HitInfo:
    def __init__(self, hit_success, killed_enemy_id = None):
        self.hit_success = hit_success
        self.killed_enemy_id = killed_enemy_id

class Unit:
    def __init__(self, pos: Vector2, team: Team):
        self.pos = pos; 
        self.team = team
        self.id = uuid.uuid1()
        self.hp = 200
        self.is_dead = False
        self.ad = 3

    def attack_in_range(self, enemies):
        ''' Try to attack enemies in range, return hitinfo '''

        # Get all enemies that are one step away
        in_range_enemies = [i for i in enemies if abs(i.pos.x - self.pos.x) + abs(i.pos.y - self.pos.y) == 1]

        if len(in_range_enemies) > 0:
            # Sort enemies by hp, then by reading order, attack first enemy
            in_range_enemies = sorted(in_range_enemies, key = lambda enemy: (enemy.hp, enemy.pos.y, enemy.pos.x))

            killed_enemy_id = None
            # If enemy dies, note it in the hitinfo returned
            if in_range_enemies[0].take_damage(self.ad):
                killed_enemy_id = in_range_enemies[0].id

            return HitInfo(True, killed_enemy_id)
            
        return HitInfo(False)

    def take_turn(self, game_manager):
        enemies = game_manager.get_all_enemy_units(self.team)

        if len(enemies) == 0: return False

        #####
        # STEP 1 - CHECK IF AN ENEMY IS ADJACENT, IF SO ATTACK AND END TURN
        #####

        hitinfo = self.attack_in_range(enemies)
        if hitinfo.hit_success:
            if hitinfo.killed_enemy_id is not None:
                game_manager.kill_unit(hitinfo.killed_enemy_id)
            return True

        #####
        # STEP 2 - TRY TO MOVE IN RANGE OF AN ENEMY
        #####
        # Get set of all squares that are in range of each target
        squares_in_range = set()
        for enemy in enemies: 
            squares_in_range.update(game_manager.get_all_moveable_squares_in_range(enemy.pos))

        # If there's nothing to do, cancel our turn
        if len(squares_in_range) == 0:
            return True

        # Move to closest available square adjacent to an enemy, attack.
        closest_move = game_manager.get_next_move(self.pos, squares_in_range)
        if closest_move is None:
            return True
        game_manager.move_unit(self, closest_move)

        hitinfo = self.attack_in_range(enemies)
        if hitinfo.hit_success:
            if hitinfo.killed_enemy_id is not None:
                game_manager.kill_unit(hitinfo.killed_enemy_id)
        return True

    def take_damage(self, damage_amount):
        ''' Takes damage. returns true if unit dies. '''
        self.hp -= damage_amount
        if self.hp <= 0:
            self.is_dead = True
        return self.is_dead

    def __repr__(self):
        return f'{self.team.name} at ({self.pos.x}, {self.pos.y}) with {self.hp} hp'

class GameManager:
    def __init__(self, grid):
        self.grid = grid
        self.rounds_completed = 0
        self.units: list[Unit] = []
        self.game_over = False
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 'G':
                    self.units.append(Unit(Vector2(x, y), Team.GOBLINS))
                elif self.grid[y][x] == 'E':
                    self.units.append(Unit(Vector2(x, y), Team.ELVES))

    def sort_units(self):
        self.units = sorted(self.units, key = lambda unit: (unit.pos.y, unit.pos.x))

    def get_all_enemy_units(self, friendly_team):
        return [i for i in self.units if i.team != friendly_team and not i.is_dead]

    def get_all_moveable_squares_in_range(self, pos: Vector2):
        positions = []
        if self.grid[pos.y-1][pos.x] == '.': positions.append(Vector2(pos.x, pos.y-1))
        if self.grid[pos.y+1][pos.x] == '.': positions.append(Vector2(pos.x, pos.y+1))
        if self.grid[pos.y][pos.x-1] == '.': positions.append(Vector2(pos.x-1, pos.y))
        if self.grid[pos.y][pos.x+1] == '.': positions.append(Vector2(pos.x+1, pos.y))
        return positions

    def move_unit(self, unit: Unit, target: Vector2):
        ''' Teleports a unit to a target. Assumes that a path has already been found '''
        unit_code = self.grid[unit.pos.y][unit.pos.x]
        if unit_code not in ['G', 'E']:
            raise Exception("Trying to move from a position that isn't a G or E")

        if self.grid[target.y][target.x] != '.':
            raise Exception("Trying to move a unit to an occupied space")

        self.grid[unit.pos.y][unit.pos.x] = '.'
        unit.pos = Vector2(target.x, target.y)
        self.grid[unit.pos.y][unit.pos.x] = 'E' if unit.team == Team.ELVES else 'G'
            

    def kill_unit(self, _id):
        ''' Kills a unit by id '''
        [unit] = [i for i in self.units if i.id == _id]
        self.grid[unit.pos.y][unit.pos.x] = '.'

    def get_next_move(self, starting_position: Vector2, ending_positions: set):
        ''' Breadth first search to find the nearest position for the starting position to move to if trying to move towards the closest ending position '''

        # Set of position to its final distance from source
        distances = {}

        visited = set([starting_position])
        queue = Queue() 

        # Tuple of position, dist to that position, path to that position
        queue.put((starting_position, 0, [starting_position]))

        while not queue.empty():
            pos, dist, path = queue.get()

            # Found one of our ends
            if pos in ending_positions:
                distances[pos] = (dist, path)

            nearby = sorted([i for i in self.get_all_moveable_squares_in_range(pos) if i not in visited], key = lambda z: (z.y, z.x))

            for square in nearby:
                visited.add(square)
                queue.put((square, dist + 1, path + [square]))

        if len(distances) == 0:
            return None

        min_dist = min(distances.values(), key = lambda x: x[0])[0]

        possible_move_towards = [p for p, d in distances.items() if d[0] == min_dist]
        final_move_towards = sorted(possible_move_towards, key = lambda unit: (unit.y, unit.x))[0]
        
        path_to_move_down = distances[final_move_towards][1]
        return path_to_move_down[1]

    def do_round(self):
        self.sort_units()

        for unit in self.units:
            if unit.is_dead: continue
            if not unit.take_turn(self):
                self.game_over = True
                return

        # Clean dead units
        self.units = [i for i in self.units if not i.is_dead]

        self.rounds_completed += 1

    def get_combined_health(self):
        return sum(i.hp for i in self.units if not i.is_dead)
        

game_manager = GameManager([list(i) for i in FileImporter.get_input("/../input/15.txt").split("\n")])

while not game_manager.game_over:
    game_manager.do_round()

print((game_manager.rounds_completed) * game_manager.get_combined_health())