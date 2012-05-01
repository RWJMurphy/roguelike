# -*- coding: utf-8 -*-

from helpers import AttrDict

__all__ = ['Trait', 'Fightable', 'Destroyable']

class Trait:
    def __init__(self, parent):
        self._parent = parent

class Fightable(Trait):
    def __init__(self, parent, health, drops=None):
        super().__init__(parent)
        self.max_health = health
        self.health = health
        if drops is None:
            drops = []
        self._drops = drops

        self.defense = 0
        self.attack = 10

    def onfought(self, attacker):
        damage = attacker.attack - self.defense
        self.health -= damage
        result = AttrDict({
            'message': "{} attacks {} for {}".format(attacker.name, self._parent.name, damage),
            'objects': [drop() for drop in self._drops],
        })
        if self.health <= 0:
            result.message += ", killing {}!".format(self._parent.name)
            self._parent.die()
        return result

class Destroyable(Trait):
    def __init__(self, parent, drops=None):
        super().__init__(parent)
        self._destroyed = False
        if drops is None:
            drops = []
        self._drops = drops

    def ondestroy(self, destroyer):
        self._parent.die()
        self._destroyed = True
        result = AttrDict({
            'message': "{} destroys the {}!".format(destroyer.name, self._parent.name),
            'objects': [drop() for drop in self._drops],
        })
        return result
