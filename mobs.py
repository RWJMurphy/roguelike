# -*- coding: utf-8 -*-

import random

from helpers import AttrDict
from objects import GameObject
import traits

__all__ = ['Mob']

class Mob(GameObject):
    def __init__(self, char, name, speed=10, x=None, y=None, z=30, blocks_movement=True, blocks_light=False):
        super().__init__(char, name, x, y, z, blocks_movement, blocks_light)
        self._speed = speed

    def tick(self, level_map):
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        movement = AttrDict({'x': dx, 'y': dy})
        if (level_map.can_move_object(self, movement)):
            level_map.move_object(self, movement)

    @staticmethod
    def peasant():
        p = Mob('@', "Peasant")
        p.add_trait(traits.Fightable(p, 10, [
            lambda: GameObject.corpse(p.name, p.x, p.y),
            lambda: GameObject.debris(p.x + random.randint(-5, 5), p.y + random.randint(-5, 5)),
            lambda: GameObject.debris(p.x + random.randint(-5, 5), p.y + random.randint(-5, 5)),
        ]))
        return p
