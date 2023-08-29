import abc
import math

from data_structures.referential_array import ArrayR
from data_structures.abstract_list import MonsterList
from data_structures.stack_adt import ArrayStack


class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass



class SimpleStats(Stats):

    def __init__(self, attack, defense, speed, max_hp) -> None:
        """Initializes an instance of the SimpleStats class.

        :param attack: Attack stat.
        :param defense: Defense stat.
        :param speed: Speed stat.
        :param max_hp: Max HP stat.
        :complexity: O(1)
        """
        self._attack = attack
        self._defense = defense
        self._speed = speed
        self._max_hp = max_hp

    def get_attack(self):
        """Returns the attack stat.

        :returns: The attack stat.
        :complexity: O(1)
        """
        return self._attack

    def get_defense(self):
        return self._defense

    def get_speed(self):
        return self._speed

    def get_max_hp(self):
        return self._max_hp

class ComplexStats(Stats):

    def __init__(

        self,
        attack_formula: ArrayR[str],
        defense_formula: ArrayR[str],
        speed_formula: ArrayR[str],
        max_hp_formula: ArrayR[str],
    ) -> None:

        """Initializes an instance of the ComplexStats class with given formulas for each stat.

        :param attack_formula: Formula for calculating attack stat.
        :param defense_formula: Formula for calculating defense stat.
        :param speed_formula: Formula for calculating speed stat.
        :param max_hp_formula: Formula for calculating max_hp stat.
        :complexity: O(1)

        all get methods run in O(n)
        """
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula

           
    def get_attack(self, level: int):
        """Calculates and returns the attack stat.

        :param level: The level for which the attack stat is calculated.
        :returns: The calculated attack stat.
        :complexity: O(n), where n is the length of the attack formula array.
        """
        formula = self.attack_formula
        stack = ArrayStack(len(formula))
        for i in range(len(formula)-1,-1,-1):
            stack.push(formula[i])
        a = stack.pop()
        if stack.is_empty():
            return level
        b = stack.pop()
        value = self.calculator(stack, level, a, b)
        return value

    def get_defense(self, level: int):
        formula = self.defense_formula
        stack = ArrayStack(len(formula))
        for i in range(len(formula)-1,-1,-1):
            stack.push(formula[i])
        a = stack.pop()
        if stack.is_empty():
            return level
        b = stack.pop()
        value = self.calculator(stack, level, a, b)
        return value

    def get_speed(self, level: int):
        formula = self.speed_formula
        stack = ArrayStack(len(formula))
        for i in range(len(formula)-1,-1,-1):
            stack.push(formula[i])
        a = stack.pop()
        if stack.is_empty():
            return level
        b = stack.pop()
        value = self.calculator(stack, level, a, b)
        return value

    def get_max_hp(self, level: int):
        formula = self.max_hp_formula
        stack = ArrayStack(len(formula))
        for i in range(len(formula)-1,-1,-1):
            stack.push(formula[i])
        a = stack.pop()
        if stack.is_empty():
            return level
        b = stack.pop()
        value = self.calculator(stack, level, a, b)
        return value

    def calculator(self, stack:ArrayStack, level:int, a, b):
        """Helper method to calculate stat value using given formula.

        :param stack: Stack containing the elements of the formula.
        :param level: The level for which the stat is calculated.
        :param a, b: Intermediate variables for calculation.
        :returns: The calculated stat value.
        :complexity: O(n), where n is the length of the formula array.
        """
        if type(a) == str:
            # a will never be the terminating element in the formula as level represents a number, not an operation
            a = level
            value = self.calculator(stack, level, a, b)
            return value
        if type(b) == str:
            a = math.sqrt(a)
            if stack.is_empty(): a
            value = self.calculator(stack, level, a, stack.pop())
            return value
        c = stack.pop()
        if type(c) != str:
            #if c is not a string, then it is a number and must be followed by an operator so the stack must not be empty
            a = (a+b+c)/3
            value = self.calculator(stack, level, a, stack.pop())
            return value
        a = self.operations(c,a,b)
        if stack.is_empty(): a
        value = self.calculator(stack, level, stack.pop)
        return value

    def operations(self, opr:str, a, b):
        """Applies the operation to the operands.

        :param opr: The operation to be applied.
        :param a, b: Operands for the operation.
        :returns: The result of the operation.
        :complexity: O(1)
    """
        if opr == "+":
            return a+b
        if opr == "/":
            return a/b
        if opr == "-":
            return a-b
        if opr == "*":
            return a*b
        if opr == "power":
            return a**b