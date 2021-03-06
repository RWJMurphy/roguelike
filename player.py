# -*- coding: utf-8 -*-

from color import Color
from mobs import Mob
import traits

__all__ = ['Player']

class Player(Mob):
    def __init__(self, action_callback, render_callback):
        super().__init__(
                char='@',
                name="Player",
                speed=5,
                blocks_light = True,
                color=Color(0, 0, 255)
            )
        self.action_callback = action_callback
        self.render_callback = render_callback
        self._inventory_max_weight = 10000
        self.add_trait(traits.Fightable(self, 99999))

    def tick(self, level_map):
        self.render_callback()
        r = self.action_callback()
        return r

    def oncollide(self, collided_with):
        if collided_with.has_trait(traits.Destroyable):
            return collided_with.ondestroy(self)
        elif collided_with.has_trait(traits.Fightable):
            return collided_with.onfought(self)
