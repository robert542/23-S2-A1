from __future__ import annotations
import abc

from stats import Stats
from elements import EffectivenessCalculator, Element

class MonsterBase(abc.ABC):

    def __init__(self, simple_mode=True, level:int=1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.


        retrieval from stats will run in O(n) if simple_mode = False as the get methods derive from complex stats rather than simple
        """
        self._level = level
        self.leveled_up = False
        if simple_mode:
            self.stats = self.get_simple_stats()
        else:
            self.stats = self.get_complex_stats()
        
        self.hp = self.stats.get_max_hp()


    def get_level(self):
        """Returns the current level of this monster instance.
        :complexity: O(1)
        """

        return self._level

    def level_up(self):
        """Increase the level of this monster instance by 1.
        :complexity: O(1)
        """
        self._level += 1
        self.leveled_up = True

    def set_level(self, new_level):
        """Allows you to set the level of the monster to a value.
        :complexity: O(1)
        """
        self._level = new_level

    def get_hp(self):
        """Get the current HP of this monster instance"""
        return self.hp

    def set_hp(self, val):
        """Set the current HP of this monster instance"""
        if type(val) != int:
            raise TypeError("val must be an integer")
        if val > self.get_max_hp():
            self.hp = self.get_max_hp()
        elif val < 0:
            self.hp = 0
        else:
            self.hp = val

    def get_attack(self):
        """Get the attack of this monster instance"""
        return self.stats.get_attack()

    def get_defense(self):
        """Get the defense of this monster instance"""
        return self.stats.get_defense()

    def get_speed(self):
        """Get the speed of this monster instance"""
        return self.stats.get_speed()

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""
        return self.stats.get_max_hp()

    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        if self.hp > 0: return True
        return False

    def attack(self, other: MonsterBase):
        """Attack another monster instance"""
        # Step 1: Compute attack stat vs. defense stat
        # Step 2: Apply type effectiveness
        # Step 3: Ceil to int
        # # Step 4: Lose HP
        
        if self.alive():
            attack = self.get_attack()
            defense = other.get_defense()
            #step 1
            if defense < attack/2:
                damage = attack - defense
            elif defense < attack: 
                damage = attack * 5/8 - defense/4
            else:
                damage = attack / 4
        
            #step 2
            elemental_multiplier = EffectivenessCalculator.get_effectiveness(Element.from_string(self.get_element()), Element.from_string(other.get_element()))
            effective_damage = damage*elemental_multiplier

            final_damage = int(effective_damage)+1

            other.remove_health(final_damage)
        


    def remove_health(self, amount):
        """Removes the amount of health specified in the amount from the monster its called on"""
        self.hp -= amount


    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""
        if self.get_evolution() != None and self.leveled_up and self.alive:
            return True
        return False

    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        hp_diff = self.get_max_hp - self.get_hp
        evolution = self.get_evolution()
        evolution.remove_health(hp_diff)
        evolution.set_level(self._level)
        return evolution
    
    def __str__(self):
        # "LV.3 Flamikin, 5/6 HP"
        return f"LV.{self.get_level()} {self.get_name()}, {self.hp}/{self.get_max_hp()} HP"

    ### NOTE
    # Below is provided by the factory - classmethods
    # You do not need to implement them
    # And you can assume they have implementations in the above methods.

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Returns the name of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_description(cls) -> str:
        """Returns the description of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_evolution(cls) -> type[MonsterBase]:
        """
        Returns the class of the evolution of the Monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_element(cls) -> str:
        """
        Returns the element of the Monster.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def can_be_spawned(cls) -> bool:
        """
        Returns whether this monster type can be spawned on a team.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_simple_stats(cls) -> Stats:
        """
        Returns the simple stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_complex_stats(cls) -> Stats:
        """
        Returns the complex stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass
