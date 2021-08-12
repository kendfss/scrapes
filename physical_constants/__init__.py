"""
Todo
    add symbols
        allow Constants().__symbol__ syntax
        μσςζη
"""
__all__ = "Constants reset".split()

import json, os

from sl4ng import tipo
from scrape import scrape, PATH, INDEX, fix_magnitude

here, this = os.path.split(__file__)
__json_path ='physical_constants-min.json'
_default_path = os.path.join(here, __json_path)

def reset():
    scrape(PATH, INDEX)

class Constant:
    def __init__(self, base, name):
        self.__base = base
        self.__name = name

    @property
    def name(self):
        return self.__name
    @property
    def value(self):
        return self.__base['value']
    @property
    def uncertainty(self):
        return self.__base['uncertainty']
    @property
    def units(self):
        return self.__base['units']
    
    # LOGIC
    def __bool__(self):
        return not self.uncertainty
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.value == other.value
        return self.value == other
    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.value < other.value
        return self.value < other
    def __gt__(self, other):
        if isinstance(other, type(self)):
            return self.value > other.value
        return self.value > other
    def __le__(self, other):
        if isinstance(other, type(self)):
            return self.value <= other.value
        return self.value <= other
    def __ge__(self, other):
        if isinstance(other, type(self)):
            return self.value >= other.value
        return self.value >= other

    # ARITHMETIC
    def __add__(self, other):
        if isinstance(other, type(self)):
            return self.value + other.value
        return self.value + other
    def __sub__(self, other):
        if isinstance(other, type(self)):
            return self.value - other.value
        return self.value - other
    def __mul__(self, other):
        if isinstance(other, type(self)):
            return self.value * other.value
        return self.value * other
    def __truediv__(self, other):
        if isinstance(other, type(self)):
            return self.value / other.value
        return self.value / other
    def __div__(self, other):
        if isinstance(other, type(self)):
            return self.value // other.value
        return self.value // other
    def __mod__(self, other):
        if isinstance(other, type(self)):
            return self.value % other.value
        return self.value % other
    def __pow__(self, other):
        if isinstance(other, type(self)):
            return self.value ** other.value
        return self.value ** other
    def __rpow__(self, other):
        if isinstance(other, type(self)):
            return other.value ** self.value
        return other ** self.value

        
    def __getitem__(self, key):
        if key == 'name':
            return self.name
        for k, v in self.__base.items():
            if key in (k, k.lower(), k.replace(' ', '_')):
                return v
        raise KeyError
    def __repr__(self):
        return "Constant(name={}, value={}, uncertainty={}, units={})".format(self.name, self.value, self.uncertainty, self.units)

class Constants:
    def __init__(self, path=_default_path):
        self.__path = path
        with open(path, 'r') as fob:
            self.__table = json.load(fob)
    def __repr__(self):
        return f"Constants(len={len(self.__table)}, path={self.__path})"
    def __getitem__(self, key):
        for k, v in self.__table.items():
            if key in (k, k.lower(), k.replace(' ', '_')):
                return Constant(v, k)
        raise KeyError
    def save(self, name='physical_constants', minified=True):
        """
        Save a modified constants table to the chosen file-name

        parameters
            name:str
                chosen file name (without extension, which defaults to json)
            minified:bool
                whether or not you would like the serial to be stripped of unnecessary whitespace
        """
        name += '-min.json' if minified else '.json'
        with open(name, 'w') as fob:
            json.dump(self.__table, fob, sort_keys=True)

if __name__ == '__main__':
    c = Constants()
    print(c)
    h = c['Planck constant']
    print(h)
    print(h['name'])
    print(h['value'])
    print(h['uncertainty'])
    print(h['units'])
    G = c['Newtonian constant of gravitation']
    print(G)
    print(G['name'])
    print(G['value'])
    print(G['uncertainty'])
    print(G['units'])
    