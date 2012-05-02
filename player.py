# -*- coding: utf-8 -*-

from color import Color
from mobs import Mob
import traits

__all__ = ['Player']

class Player(Mob):
    def __init__(self):
        super().__init__(
                char='@',
                name="Player",
                blocks_light = True,
                color=Color(0, 0, 255)
            )
        self.add_trait(traits.Fightable(self, 99999))

    def tick(self, level_map):
        pass

    def oncollide(self, collided_with):
        if collided_with.has_trait(traits.Destroyable):
            return collided_with.ondestroy(self)
        elif collided_with.has_trait(traits.Fightable):
            return collided_with.onfought(self)
