# -*- coding: utf-8 -*-

class GameConfig:
    instance = None

    def __init__(self):
        self.game_name = "DEITY RL"
        self.world_width = 100
        self.world_height = 100

    @staticmethod
    def load():
        if GameConfig.instance == None:
            GameConfig.instance = GameConfig()
        return GameConfig.instance
