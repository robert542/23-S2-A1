from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR
from data_structures.queue_adt import CircularMonsterQueue
from data_structures.abstract_list import MonsterList

if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode():

        HP = lambda x: x.get_hp()
        ATTACK = lambda x: x.get_attack()
        DEFENSE = lambda x: x.get_defense()
        SPEED = lambda x: x.get_speed()
        LEVEL = lambda x: x.get_level()

    TEAM_LIMIT = 6


    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:
        # Add any preinit logic here.
        self.team = MonsterList()
        self.descending = True

        self.name = kwargs.get('team_name', None)

        self.sort_key = kwargs.get('sort_key', None)

        self.team_mode = team_mode
        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly()
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually()
        elif selection_mode == self.SelectionMode.PROVIDED:
            provided_monsters = kwargs.get('provided_monsters', None)
            self.select_provided(provided_monsters)
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")

    def add_to_team(self, monster: MonsterBase):
        if self.team_mode == self.TeamMode.FRONT:
            self.team.insert(0, monster)
        elif self.team_mode == self.TeamMode.BACK:
            self.team.append(monster)
        elif self.team_mode == self.TeamMode.OPTIMISE:
            self.team.insert(0,monster)
            self.team.sort(self.descending, self.sorting_key) 

    def retrieve_from_team(self) -> MonsterBase:
        for i in range(len(self.team)):
            monster = self.team[i]
            if monster.alive():
                self.team.delete_at_index(i)
                return monster
        return None


    def special(self,**kwargs) -> None:
        if self.team_mode == self.TeamMode.FRONT:
            self.team.front_swap(2)
        elif self.team_mode == self.TeamMode.BACK:
            self.team.flip_halves()
        elif self.team_mode == self.TeamMode.OPTIMISE:

            if self.sorting_key == None:
                raise ValueError("Sorting stat must be provided for Optimize team mode")
            if type(self.sorting_key) != self.SortMode:
                raise TypeError("sorting key must be of type SortMode")
            self.descending = not self.descending
            self.team.sort(self.descending, self.sorting_key)

    def regenerate_team(self) -> None:
        for i in range(len(self.team)):
            self.team[i].set_hp(self.team[i].get_max_hp())
        
    def select_randomly(self):
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x]())
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

        How many monsters are there? 2
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 38
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 2
        This monster cannot be spawned.
        Which monster are you spawning? 1
        """


        valid = False
        while not valid:
            team_size = input("How big is your team: ")
            try:
                team_size = int(team_size)
                if team_size <= self.TEAM_LIMIT:
                    valid = True
                else:
                    print(f"The team size you choose must not exceed {self.TEAM_LIMIT}!\n")
            except:
                print(f"Team size must be given as an integer with a maximum size of {self.TEAM_LIMIT}\n")
        monsters = get_all_monsters()
        for _ in range(team_size):
            valid = False
            print("MONSTERS are:")
            for i in range(len(monsters)):
                monster = monsters[i]
                if monster.can_be_spawned():
                    spawn_stat = "✔️"
                else:
                    spawn_stat = "❌"
                print(f"{i+1}: {monster.get_name()} [{spawn_stat}]")
            
            while not valid:
                choice = input("Which monster are you spawning?")
                try:
                    choice = int(choice)
                    if choice > len(monster) or choice < 1:
                        print("Your number does not corelate to any monster on the list, choose again.")
                    elif monsters.choice.can_be_spawned() != True:
                        print("This monster cannot be spawned.")
                    else:
                        self.team.append(monsters[choice]())
                        valid = True
                except:
                    print("Your input must be an integer, try again")
                
    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]
        """
        if provided_monsters == None:
            raise ValueError("You need to pass an array of type MonsterBase")
        for monster in provided_monsters:
            if self.team.is_full():
                print("The list you provided had more monsters than the allowed total, not all monsters were added to your team")
                break
            if monster.can_be_spawned():
                self.add_to_team(monster)

    def __len__(self):
        return self.team.get_length()

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

    def get_team(self):
        return self.team
    
    def __str__(self):
        return f"{self.name}({len(self.get_team())})"
    
if __name__ == "__main__":
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )
    print(team)
    while len(team):
        print(team.retrieve_from_team())
