# -*- coding: utf-8 -*-

class GameObject:
    def __init__(self, char, name, x=None, y=None, z=20, blocks_movement=True, blocks_light=False):
        self.char = char
        self.name = name

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
        raise AttributeError

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
    def debris(x=None, y=None, name="Debris"):
        return GameObject('*', name, x, y, blocks_movement=False)

    @staticmethod
    def corpse(name=None, x=None, y=None):
        if name is None:
            name = "corpse"
        else:
            name = name + " corpse"
        return GameObject('%', name, x, y, blocks_movement=False)
