# -*- coding: utf-8 -*-
import math
import random

from objects import GameObject
import traits

__all__ = ['Map', 'Tile']

class Map:
    def __init__(self, width=None, height=None, message_callback=None):
        self._width = width
        self._height = height
        # self._map[x][y] = [Tile, Object, etc.]
        self._map = [[[] for y in range(self._height)] for x in range(self._width)]
        self._objects = []
        self._message = message_callback

    def restack(self):
        for x in range(self._width):
            for y in range(self._height):
                for t in self._map[x][y]:
                    if not t._alive:
                        try:
                            self._objects.remove(t)
                        except:
                            pass
                        self._map[x][y].remove(t)
                self._map[x][y].sort(key=lambda tile: tile.z, reverse=True)

    def get_tile(self, x, y, pop=False):
        for obj in self._map[x][y]:
            if isinstance(obj, Tile):
                if pop:
                    self._map[x][y].remove(obj)
                return obj
        return None

    def set_tile(self, x, y, tile):
        self.get_tile(x, y, True)
        self._map[x][y].insert(0, tile)

    def get_move_cost(self, x, y):
        return sum(item.move_cost for item in self._map[x][y])

    def insert_objects(self, obj):
        if obj == None:
            return
        if isinstance(obj, list):
            for o in obj:
                self.insert_objects(o)
            return
        self._map[obj.x][obj.y].append(obj)
        self._objects.append(obj)

    def can_move_object(self, obj, movement):
        new_x, new_y = obj.x + movement.x, obj.y + movement.y
        if new_x < 0 or new_y < 0 or new_x >= self._width or new_y >= self._height:
            return False
        dest_blocked = True in [x.blocks_movement for x in self._map[new_x][new_y]]
        return not dest_blocked

    def move_object(self, obj, movement):
        new_x, new_y = obj.x + movement.x, obj.y + movement.y
        self._map[obj.x][obj.y].remove(obj)
        obj.xy(new_x, new_y)
        self._map[obj.x][obj.y].append(obj)

        distance = math.sqrt(movement.x**2 + movement.y**2)
        cost = self.get_move_cost(new_x, new_y) * distance
        return cost

    def grab_object(self, obj):
        items = self._map[obj.x][obj.y]
        for i in items:
            if i.has_trait(traits.Carryable):
                r = obj.ongrab(i)
                self.message(r.message)
                if r.success:
                    i.ongrabbed(obj)
                    items.remove(i)
                    return True
                else:
                    break
        return False

    def object_act_in_direction(self, obj, direction):
        new_x, new_y = obj.x + direction.x, obj.y + direction.y
        results = []
        cost = 0
        try:
            targets = self._map[new_x][new_y]
        except IndexError:
            return 0

        for t in targets:
            results.append(obj.oncollide(t))
        for r in results:
            if r is not None:
                cost += r.cost
                self.message(r.message)
                self.insert_objects(r.objects)
        return cost

    def get_view(self, center_x, center_y, width, height):
        if width > self._width:
            width = self._width
        if height > self._height:
            height = self._height

        top = center_y - int(height/2)
        left = center_x - int(width/2)
        if top < 0:
            top = 0
        elif top > (self._height - height):
            top = self._height - height

        if left < 0:
            left = 0
        elif left > (self._width - width):
            left = self._width - width

        view = [[ self._map[x][y][0] for x in range(left, left+width)] for y in range(top, top+height)]
        return view

    def tick(self):
        for o in self._objects:
            o.tick(self)

    def set_message(self, callback):
        self._message = callback

    def message(self, msg):
        if self._message:
            self._message(msg)

class Tile(GameObject):
    def __init__(self, char, name="", x=None, y=None, zindex = 0, blocks_movement=False, blocks_light=False, color=None, move_cost=1):
        super().__init__(char, name, x, y, z=zindex, blocks_movement=blocks_movement, blocks_light=blocks_light, color=color, move_cost=move_cost)

    @staticmethod
    def floor(x=None, y=None):
        return Tile('.', "Floor", x, y, color=(100, 100, 0))

    @staticmethod
    def wall(x=None, y=None):
        tile = Tile('#', "Wall", x, y, 100, blocks_movement=True, blocks_light=True)
        tile.add_trait(traits.Destroyable(
                tile,
                [ 
                    lambda: Tile.floor(tile.x, tile.y),
                    lambda: GameObject.debris(tile.x + random.randint(-5, 5), tile.y + random.randint(-5, 5)),
                    lambda: GameObject.debris(tile.x + random.randint(-5, 5), tile.y + random.randint(-5, 5)),
                    lambda: GameObject.debris(tile.x + random.randint(-5, 5), tile.y + random.randint(-5, 5)),
                    lambda: GameObject.debris(tile.x + random.randint(-5, 5), tile.y + random.randint(-5, 5)),
                ]
            ))
        return tile

    @staticmethod
    def empty(x=None, y=None):
        return Tile(' ', "A vast empty gulf of nothingness.", x, y, blocks_movement=True)

    @staticmethod
    def door(x=None, y=None):
        tile = Tile('+', "Door", x, y)
        tile.add_trait(traits.Openable(tile))
        tile.add_trait(traits.Destroyable(
            tile,
            [
                lambda: Tile.floor(tile.x, tile.y),
                lambda: GameObject.debris(tile.x + random.randint(-2, 2), tile.y + random.randint(-2, 2)),
                lambda: GameObject.debris(tile.x + random.randint(-2, 2), tile.y + random.randint(-2, 2)),
            ]
        ))
        return tile

