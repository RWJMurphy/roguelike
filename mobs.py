# -*- coding: utf-8 -*-

import random

from helpers import AttrDict
from objects import GameObject
import traits

__all__ = ['Mob']

class Mob(GameObject):
    def __init__(self, char, name, speed=1, x=None, y=None, z=30, blocks_movement=True, blocks_light=False, color=None):
        super().__init__(char, name, x, y, z, blocks_movement, blocks_light, color)
        self._speed = speed # action points per tick
        self._energy = 0.0
        self._inventory = []
        self._inventory_current_weight = 0
        self._inventory_max_weight = 0

    def restore_energy(self, ticks=1):
        self._energy += self._speed * ticks

    def tick(self, level_map):
        roll = random.randrange(100)
        if 0 <= roll < 10:
            item = level_map.grab_object(self)
        elif 10 <= roll <= 90:
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            movement = AttrDict({'x': dx, 'y': dy})
            if (level_map.can_move_object(self, movement)):
                self._energy -= level_map.move_object(self, movement)
        elif 90 <= roll < 100:
            self._energy -= self._speed

    def ongrab(self, target):
        if self._inventory_current_weight + target._weight > self._inventory_max_weight:
            result = AttrDict({
                'success': False,
                'message': '{} cannot pick up {}, it is too heavy'.format(self.name, target._parent.name),
            })
            self._energy -= 1 + target._weight * 0.05
        else:
            self._inventory.append(target)
            self._inventory_current_weight += target._weight
            result = AttrDict({
                'success': True,
                'message': '{} picks up {}'.format(self.name, target._parent.name),
            })
            self._energy -= 1 + target._weight * 0.1
        return result

    @staticmethod
    def peasant():
        p = Mob('@', "Peasant")
        p.add_trait(traits.Fightable(p, 10, [
            lambda: GameObject.corpse(p.name, p.x, p.y),
            lambda: GameObject.debris(p.x + random.randint(-2, 2), p.y + random.randint(-2, 2), color=(255, 0, 0)),
            lambda: GameObject.debris(p.x + random.randint(-2, 2), p.y + random.randint(-2, 2), color=(255, 0, 0)),
        ]))
        return p

    def dog():
        d = Mob('d', "Dog")
        d.add_trait(traits.Fightable(d, 5, [
            lambda: GameObject.corpse(d.name, d.x, d.y),
            lambda: GameObject.debris(d.x + random.randint(-2, 2), d.y + random.randint(-2, 2), color=(255, 0, 0))
        ]))
        d.add_trait(traits.Hostile(d))
        d.add_trait(traits.MeleeAttack(d, lambda: random.randint(4, 6)))
        return d
