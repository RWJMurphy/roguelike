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

        self.defense = lambda: 0
        self.attack = lambda: 10

    def onfought(self, attacker):
        damage = attacker.attack() - self.defense()
        self.health -= damage
        result = AttrDict({
            'message': "{} attacks {} for {}".format(attacker.name, self._parent.name, damage),
            'objects': [drop() for drop in self._drops],
        })
        if self.health <= 0:
            result.message += ", killing {}!".format(self._parent.name)
            self._parent.die()
        return result

class Hostile(Trait):
    def __init__(self, parent):
        super().__init__(parent)

    def tick(self, level_map):
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        movement = AttrDict({'x': dx, 'y': dy})
        if (level_map.can_move_object(self, movement)):
            level_map.move_object(self, movement)

class MeleeAttack(Trait):
    def __init__(self, parent, damage_function):
        super().__init__(parent)
        self.attack = damage_function

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

class Openable(Trait):
    def __init__(self, parent, open=False, state_chars=None):
        super().__init__(parent)

        if state_chars is None:
            state_chars = "_+"

        self._open_char = state_chars[0]
        self._closed_char = state_chars[1]

        self._open = not open
        self.ontoggle()

    def ontoggle(self):
        self._open = not self._open

        self._parent.blocks_movement = not self._open
        if self._open:
            self._parent.char = self._open_char
        else:
            self._parent.char = self._closed_char
        return True
