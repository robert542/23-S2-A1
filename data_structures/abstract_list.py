""" List ADT. Defines a generic abstract list with the standard methods. """

from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from data_structures.referential_array import ArrayR
T = TypeVar('T')

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev'
__docformat__ = 'reStructuredText'

class List(ABC, Generic[T]):
    """ Abstract class for a generic List. """
    def __init__(self) -> None:
        """ Basic List object initialiser. """
        self.length = 0

    @abstractmethod
    def __getitem__(self, index: int) -> T:
        """ Magic method. Return the element at a given position. """
        pass

    @abstractmethod
    def __setitem__(self, index: int, item: T) -> None:
        """ Magic method. Insert the item at a given position. """
        pass

    def __len__(self) -> int:
        """ Return the size of the list. """
        return self.length

    def __str__(self):
        """ Magic method constructing a string representation of the list object. """
        result = '['
        for i in range(len(self)):
            if i > 0:
                result += ', '
            result += str(self[i]) if type(self[i]) != str else "'{0}'".format(self[i])
        result += ']'
        return result

    def append(self, item: T) -> None:
        """ Append a new item to the end of the list. """
        self.insert(len(self), item)
        self.length +=1

    @abstractmethod
    def insert(self, index: int, item: T) -> None:
        """ Insert an item at a given position. """
        pass

    def remove(self, item: T) -> None:
        """ Remove an item from the list. """
        index = self.index(item)
        self.delete_at_index(index)

    @abstractmethod
    def delete_at_index(self, index: int) -> T:
        """ Delete item at a given position. """
        pass

    @abstractmethod
    def index(self, item: T) -> int:
        """ Find the position of a given item in the list. """
        pass

    def is_empty(self) -> bool:
        """ Check if the list of empty. """
        return len(self) == 0

    def clear(self):
        """ Clear the list. """
        self.length = 0

class MonsterList(List):
    
    def __init__(self) -> None:
        self.length = 0
        self.array = ArrayR(0)
    
    def __getitem__(self, index: int) -> T:
        return self.array[index]
    
    def __setitem__(self, index: int, item: T) -> None:
        self.array[index] = item

    def insert(self, index: int, item: T) -> None:
        if index > len(self.array) or index < 0:
            raise ValueError("To insert a value into a list you must provide an index in the range of the list")
        
        new_array = ArrayR(len(self.array)+1)
        for i in range(index):
            new_array[i] = self.array[i]
        new_array[index] = item
        for i in range(index+1, len(self.array)+1):
            new_array[i] = self.array[i]
        self.array = new_array
        self.length +=1

    def delete_at_index(self, index: int) -> T:
        if index > len(self.array) or index < 0:
            raise ValueError("To delete a value in the list you must provide an index in the range of the list")
        
        new_array = ArrayR(len(self.array)-1)
        for i in range(index):
            new_array[i] = self.array[i]
        for i in range(index,len(self.array)-1):
            new_array[i] = self.array[i+1]
        self.array = new_array
        self.length-=1

    def index(self, item: T, strict: bool=False) -> int:
        #will return the index of item if found in list, if not found, None will be returned unless strcit is set to True
        for i in range(len(self.array)):
            if self.array[i] == item:
                return i
        if strict:
            raise LookupError("This item does not exist in this list")
        return None
    
    def __add__(self, other_list):
        if type(other_list) != type(self):
            raise TypeError("You can only add a list to a list")
        self_copy = self.array
        for i in other_list:
            self_copy.append(other_list[i])
        return self_copy

    def sort(self, descending:bool, sort_func):
        #sorts in either ascending or decending order. should really only be used when adding in optimized mode to utilize incremental nature
        values = self.array

        # Bubble sort values
        n = len(values)
        for mark in range(n-1, 0, -1):
            swapped = False
            for i in range(mark):
                if descending:
                    if sort_func(values[i]) < sort_func(values[i + 1]):
                        temp = values[i + 1]
                        values[i + 1] = values[i]
                        values[i] = temp
                        swapped = True
                else:
                    if sort_func(values[i]) > sort_func(values[i + 1]):
                        temp = values[i + 1]
                        values[i + 1] = values[i]
                        values[i] = temp
                        swapped = True
            if not swapped:
                break

    def front_swap(self, dist):
        #dist is the difference between the front and the value being swapped
        temp = self.array[self.front]
        self.array[self.front] = self.array[(self.front+dist)%len(self.array)]
        self.array[(self.front+dist)%len(self.array)] = temp

    def flip_halves(self):
        #take out of queue form
        values = self.array
        
        front_len = len(values)//2
        front_part = MonsterList(front_len)
        back_part = MonsterList(self.length-front_len)
        for i in range(self.length):
            if i <= front_len-1:
                front_part.append(values[i])
            else:
                back_part.insert(0,values[i])
        self.array =  back_part + front_part

                    
    def get_array(self):
        return self.array