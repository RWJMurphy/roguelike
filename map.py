# -*- coding: utf-8 -*-

class Map:
    def __init__(self, width=None, height=None):
        self._width = width
        self._height = height
        # self._map[x][y] = [Tile, Object, etc.]
        self._map = [[[] for y in range(self._height)] for x in range(self._width)]
        self._objects = []

    def generate(self, player=None, objects=None, mobs=None):
        for y in range(self._height):
            for x in range(self._width):
                self.set_tile(x, y, Tile.floor())

        self.insert_objects([player, objects, mobs])

    def restack(self):
        for x in range(self._width):
            for y in range(self._height):
                self._map[x][y].sort(key=lambda tile: tile.z, reverse=True)

    def set_tile(self, x, y, tile):
        for obj in self._map[x][y]:
            if isinstance(obj, Tile):
                self._map[x][y].remove(obj)
                break
        self._map[x][y].insert(0, tile)

    def insert_objects(self, obj):
        if obj == None:
            return
        if isinstance(obj, list):
            for o in obj:
                self.insert_objects(o)
            return
        self._map[obj.x][obj.y].append(obj)
        self._objects.append(obj)

    def move_object(self, obj, movement):
        self._map[obj.x][obj.y].remove(obj)
        obj.xy(obj.x + movement.x, obj.y + movement.y)
        self._map[obj.x][obj.y].append(obj)

    def get_view(self, center_x, center_y, width, height):
        self.restack()
        top = center_y - int(height/2)
        left = center_x - int(width/2)
        view = [[ self._map[x][y][0].char for x in range(left, left+width)] for y in range(top, top+height)]
        return view

class Tile:
    def __init__(self, char, name=""):
        self.char = char
        self.name = name
        self.z = 0

    @staticmethod
    def floor():
        return Tile('.', "Floor")
