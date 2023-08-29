from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element

from data_structures.referential_array import ArrayR
from data_structures.abstract_list import MonsterList
from data_structures.queue_adt import CircularMonsterQueue
from data_structures.bset import BSet

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10



    def __init__(self, battle: Battle|None=None) -> None:
        self.battle = battle or Battle(verbosity=0)
        self.battle_count = 0
        self.dead_teams = MonsterList()
        self.seen_elements = BSet()

    def __iter__(self):
        self.iter_index = 0  # Initialize iterator index
        return self

    def __next__(self):
        if not self.battles_remaining():
            raise StopIteration  # Stop iterating if no more battle
        result = self.next_battle()  # Call your existing next_battle method
        self.iter_index += 1  # Increment iterator index

        return result  # return the result of the battle

    def set_my_team(self, team: MonsterTeam) -> None:
        # Generate the team lives here too.
        self.player_team = team
        self.player_lives = self.MAX_LIVES

    def generate_teams(self, n: int) -> None:
        
        enemy_list = CircularMonsterQueue(n)
        enemy_lives = CircularMonsterQueue(n)

        for i in range(n):
            new_team = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM, team_name = i)
            enemy_lives.append(RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES))
            enemy_list.append(new_team)
        self.tower_teams = enemy_list
        self.tower_lives = enemy_lives
        
    def battles_remaining(self) -> bool:
        if self.player_lives == 0:
            return False
        for i in range(self.tower_lives.get_length()):
            if self.tower_lives.export()[i] > 0:
                return True
        return False

    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        print("NEXT BATTLE")

        #lives and team served from team tower
        enemy_team = self.tower_teams.serve()
        enemy_lives = self.tower_lives.serve()

        #elements in upcoming battler are collected
        battle_set = BSet()
        monsters = enemy_team.get_team()
        for i in range(len(monsters)):
            battle_set.add(Element.from_string(monsters[i].get_element()).value)
        for i in range(len(self.player_team.get_team())):
            battle_set.add(Element.from_string(self.player_team.get_team()[i].get_element()).value)
        #both teams are regenerated
        self.player_team.regenerate_team()
        enemy_team.regenerate_team()

        #battle simulated
        battle_result = self.battle.battle(self.player_team, enemy_team)

        #seen elements updated
        self.seen_elements = self.seen_elements.union(battle_set)

        #draw loses botha life
        if battle_result == Battle.Result.DRAW:
            self.player_lives -= 1
            enemy_lives -= 1
        #if team 1 wins, enemy loses a life
        elif battle_result == Battle.Result.TEAM1:
            enemy_lives -= 1
        #otherwise enemy won and player loses a life
        else:
            self.player_lives -= 1
        #results are recorded for return (results, player_team, enemy_team, player lives, enemy lives)
        results = (battle_result, self.player_team, enemy_team, self.player_lives, enemy_lives)
        #add enemy to dead teams list, not really useful but good to keep
        if enemy_lives == 0:
            self.dead_teams.append(enemy_team)
        else:
            self.tower_teams.append(enemy_team)
            self.tower_lives.append(enemy_lives)

        return results   

    def out_of_meta(self) -> ArrayR[Element]:
        next_battle_set = BSet()
        index = (self.battle_count-len(self.dead_teams))%len(self.tower_teams) 
        monsters = self.tower_teams[index].get_team()
        for i in range(len(monsters)):
            next_battle_set.add(Element.from_string(monsters[i].get_element()).value)
        for i in range(len(self.player_team.get_team())):
            next_battle_set.add(Element.from_string(self.player_team.get_team()[i].get_element()).value)
        dif =  self.seen_elements.difference(next_battle_set)
        valid = MonsterList()
        for element in Element:
            if element.value in dif:
                valid.append(element)
        return valid.get_array()

    def sort_by_lives(self):
        # 1054 ONLY
        raise NotImplementedError

def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError

if __name__ == "__main__":

    RandomGen.set_seed(129371)

    bt = BattleTower(Battle(verbosity=3))
    bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM, team_name = "Robert"))
    bt.generate_teams(3)
    

    for result, player_team, tower_team, player_lives, tower_lives in bt:
        print(result, player_team, tower_team, player_lives, tower_lives)
