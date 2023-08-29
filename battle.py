from __future__ import annotations
from enum import auto
from typing import Optional

from base_enum import BaseEnum
from team import MonsterTeam


class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:
        self.verbosity = verbosity


    def process_turn(self) -> Optional[Battle.Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed.
        """
        #Get action from each team
        t1_action = self.team1.choose_action(self.out1, self.out2)
        t2_action = self.team2.choose_action(self.out2, self.out1)
        
        #execute special move or swap for team 1
        if t1_action == Battle.Action.SPECIAL:
            self.team1.special()
        elif t1_action == Battle.Action.SWAP:
            self.team1.add_to_team(self.out1)
            self.out1 = self.team1.retrieve_from_team()
        #execute special move or swap for team 2
        if t2_action == Battle.Action.SPECIAL:
            self.team2.special()
        elif t2_action == Battle.Action.SWAP:
            self.team2.add_to_team(self.out2)
            self.out2 = self.team2.retrieve_from_team()
        #Deals with if both teams attack
        if t1_action == Battle.Action.ATTACK and t2_action == Battle.Action.ATTACK:
            if self.out1.get_speed() == self.out2.get_speed():
                self.out1.attack(self.out2)
                self.out2.attack(self.out1)
            if self.out1.get_speed() > self.out2.get_speed():
                self.out1.attack(self.out2)
                self.out2.attack(self.out1)
            else:
                self.out2.attack(self.out1)
                self.out1.attack(self.out2)
        #if only one team attacks
        elif t1_action == Battle.Action.ATTACK:
            self.out1.attack(self.out2)
        else: self.out2.attack(self.out1)
        
        #if both are alive after the attacks, 1 health point is subtracted from both
        if self.out1.alive() and self.out2.alive():
            self.out1.remove_health(1)
            self.out2.remove_health(1)

        #evolves pokemon if alive
        if self.out1.ready_to_evolve():
            self.out1=self.out1.evolve()
        if self.out1.ready_to_evolve():
            self.out1=self.out1.evolve()
        #if either are dead, returns next alive monster from team queue
        #returns None if no monsters in team queue are alive
        if not self.out1.alive:
            self.team1.add_to_team(self.out1)
            self.out1 = self.team1.retrieve_from_team()
        if not self.out2.alive:
            self.team2.add_to_team(self.out2)
            self.out2 = self.team2.retrieve_from_team()

        #give final return based on value of out1 and out2
        if self.out1 == None or self.out2 == None:
            if self.out1 == None:
                if self.out2 == None:
                    return self.Result.DRAW
                return self.Result.TEAM2
            return self.Result.TEAM1
        return None


    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = self.team1.retrieve_from_team()
        self.out2 = self.team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        # Add any postgame logic here.
        return result

if __name__ == "__main__":
    t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    b = Battle(verbosity=3)
    print(b.battle(t1, t2))
