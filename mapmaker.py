# -*- coding: utf-8 -*-
import random

from map import Map, Tile

__all__ = ['MapMaker']

class MapMaker:
    def __init__(self, seed=None):
        self.random = random.Random(seed)

    def generate(self, width, height):
        the_map = Map(width, height)
        for y in range(height):
            for x in range(width):
                if x in (0, width-1) or y in (0, height-1):
                    tile = Tile.empty()
                else:
                    tile = Tile.floor()
                the_map.set_tile(x, y, tile)

        # buildings
        for i in range(self.random.randrange(20, 50)):
            room_width = self.random.randrange(4, 10)
            room_height = self.random.randrange(4, 10)
            left = self.random.randrange(width - room_width)
            top = self.random.randrange(height - room_height)
            self.draw_box(the_map, left, top, room_width, room_height)

        return the_map

    def draw_box(self, the_map, left, top, width, height):
        self.draw_horizontal_line(the_map, left, top, left + width)
        self.draw_horizontal_line(the_map, left, top + height, left + width)
        self.draw_vertical_line(the_map, left, top, top + height)
        self.draw_vertical_line(the_map, left + width, top, top + height)

    def draw_horizontal_line(self, the_map, x1, y1, x2):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            the_map.set_tile(x, y1, Tile.wall())

    def draw_vertical_line(self, the_map, x1, y1, y2):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            the_map.set_tile(x1, y, Tile.wall())

