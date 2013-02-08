# -*- coding: utf-8 -*-

from color import Color
import traits

__all__ = ['GameObject']

class GameObject:
    def __init__(self, char, name, x=None, y=None, z=20, blocks_movement=True, blocks_light=False, color=None):
        self.char = char
        self.name = name

        if color is None:
            color = Color(255, 255, 255)
        elif isinstance(color, tuple):
            if len(color) == 3:
                color = Color(*color)
            else:
                raise ValueError("If color is a tuple, it must be a 3 tuple")
        elif not isinstance(color, Color):
            raise ValueError("color must be a Color() instance, or a 3 tuple")
        self.color = color

        self.x = x
        self.y = y
        self.z = z

        self.blocks_movement = blocks_movement
        self.blocks_light = blocks_light

        self._traits = []

        self._alive = True

    def __getattr__(self, attr):
        for trait in self._traits:
            if hasattr(trait, attr):
                return getattr(trait, attr)
        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, attr))

    def xy(self, x=None, y=None):
        if x != None or y != None:
            if x != None:
                self.x = x
            if y != None:
                self.y = y
        else:
            return (self.x, self.y)

    def add_trait(self, trait):
        self._traits.append(trait)

    def get_trait(self, trait_class):
        return [trait for trait in self._traits if isinstance(trait, trait_class)]

    def has_trait(self, trait_class):
        return True in [isinstance(trait, trait_class) for trait in self._traits]
    
    def die(self):
        self._alive = False

    def tick(self, level_map):
        pass
    
    @staticmethod
    def debris(x=None, y=None, name="Debris", color=None):
        d = GameObject('*', name, x, y, blocks_movement=False, color=color)
        d.add_trait(traits.Carryable(d, 5))
        return d

    @staticmethod
    def corpse(name=None, x=None, y=None, color=Color(122, 0, 0)):
        if name is None:
            name = "corpse"
        else:
            name = name + " corpse"
        c = GameObject('%', name, x, y, blocks_movement=False, color=color)
        c.add_trait(traits.Carryable(c, 100))
        return c
