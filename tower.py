from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element

from data_structures.referential_array import ArrayR
from data_structures.abstract_list import MonsterList
from data_structures.bset import BSet

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        self.battle = battle or Battle(verbosity=0)
        self.battle_count = 0
        self.dead_teams = MonsterList()
        self.seen_elements = BSet()


    def set_my_team(self, team: MonsterTeam) -> None:
        # Generate the team lives here too.
        self.player_team = team
        self.player_lives = self.MAX_LIVES

    def generate_teams(self, n: int) -> None:
        
        enemy_list = MonsterList()
        enemy_lives = MonsterList

        for i in range(len(enemy_list)):
            new_team = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
            enemy_lives.append(RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES))
            enemy_list.append(new_team)
        self.tower_teams = enemy_list
        self.tower_lives = enemy_lives
        
    def battles_remaining(self) -> bool:
        if self.player_lives <= 0:
            return False
        for i in range(len(self.tower_lives)):
            if self.tower_lives[i] > 0:
                True
        return False

    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        
        index = (self.battle_count-len(self.dead_teams))%len(self.tower_teams) 
        enemy_team = self.tower_teams[index]
        battle_set = BSet()
        monsters = enemy_team.get_team()
        for i in range(len(monsters)):
            battle_set.add(monsters[i].get_element())
        for i in range(len(self.player_team.get_team())):
            battle_set.add(self.player_team.get_team()[i])

        self.player_team.regenerate_team()
        enemy_team.regenerate_team()
        battle_result = self.battle(self.player_team, enemy_team)

        self.seen_elements = self.seen_elements.union(battle_set)


        if battle_result == Battle.Result.DRAW:
            self.player_lives -= 1
            self.tower_lives[index] -= 1
        elif battle_result == Battle.Result.TEAM1:
            self.tower_lives[index] -= 1
        else:
            self.player_lives -= 1
        results = (battle_result, self.player_team, enemy_team, self.player_lives, self.tower_lives[index])
        if self.tower_lives[index] == 0:
            self.dead_teams.append(self.tower_teams[index])
            self.tower_teams.delete_at_index(index)
            self.tower_lives.delete_at_index(index)   
        
        return results   

    def out_of_meta(self) -> ArrayR[Element]:
        next_battle_set = BSet()
        index = (self.battle_count-len(self.dead_teams))%len(self.tower_teams) 
        monsters = self.tower_teams[index].get_team()
        for i in range(len(monsters)):
            next_battle_set.add(monsters[i].get_element())
        for i in range(len(self.player_team.get_team())):
            next_battle_set.add(self.player_team.get_team()[i].get_element())
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
    bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
    bt.generate_teams(3)

    for result, my_team, tower_team, player_lives, tower_lives in bt:
        print(result, my_team, tower_team, player_lives, tower_lives)
