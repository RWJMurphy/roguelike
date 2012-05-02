# -*- coding: utf-8 -*-
import random

from map import Map, Tile
from mobs import Mob

__all__ = ['MapMaker']

class MapMaker:
    def __init__(self, seed=None):
        self.random = random.Random(seed)

    def generate(self, width, height):
        the_map = Map(width, height)
        for y in range(height):
            for x in range(width):
                if x in (0, width-1) or y in (0, height-1):
                    tile = Tile.empty(x, y)
                else:
                    tile = Tile.floor(x, y)
                the_map.set_tile(x, y, tile)

        # buildings
        for i in range(self.random.randrange(20, 50)):
            room_width = self.random.randrange(4, 10)
            room_height = self.random.randrange(4, 10)
            left = self.random.randrange(width - room_width)
            top = self.random.randrange(height - room_height)
            self.draw_box(the_map, left, top, room_width, room_height, Tile.wall)
            door_side = random.randrange(4)
            if door_side == 0: # top
                offset = 1 + random.randrange(room_width - 2)
                door_x = left + offset
                door_y = top
            elif door_side == 1: # bottom
                offset = 1 + random.randrange(room_width - 2)
                door_x = left + offset
                door_y = top + room_height
            elif door_side == 2: # left
                offset = 1 + random.randrange(room_height - 2)
                door_x = left
                door_y = top + offset
            elif door_side == 3: # right
                offset = 1 + random.randrange(room_height - 2)
                door_x = left + room_width
                door_y = top + offset
            the_map.set_tile(door_x, door_y, Tile.door(door_x, door_y))

        # peasants
        objects = []
        for i in range(self.random.randrange(10, 100)):
            p = Mob.peasant()
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            p.xy(x, y)
            objects.append(p)

        the_map.insert_objects(objects)

        return the_map

    def draw_box(self, the_map, left, top, width, height, drawable=None):
        self.draw_horizontal_line(the_map, left, top, left + width, drawable)
        self.draw_horizontal_line(the_map, left, top + height, left + width, drawable)
        self.draw_vertical_line(the_map, left, top, top + height, drawable)
        self.draw_vertical_line(the_map, left + width, top, top + height, drawable)

    def draw_horizontal_line(self, the_map, x1, y1, x2, drawable=None):
        if drawable is None:
            drawable = Tile.wall
        for x in range(min(x1, x2), max(x1, x2) + 1):
            the_map.set_tile(x, y1, drawable(x, y1))

    def draw_vertical_line(self, the_map, x1, y1, y2, drawable=None):
        if drawable is None:
            drawable = Tile.wall
        for y in range(min(y1, y2), max(y1, y2) + 1):
            the_map.set_tile(x1, y, drawable(x1, y))

