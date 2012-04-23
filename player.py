# -*- coding: utf-8 -*-

class Player:
    def __init__(self):
        self.char = '@'
        self.x = None
        self.y = None
        self.z = 10

        self.blocks_movement = True
        self.blocks_light = True
    
    def xy(self, x=None, y=None):
        if x != None or y != None:
            if x != None:
                self.x = x
            if y != None:
                self.y = y
        else:
            return (self.x, self.y)

