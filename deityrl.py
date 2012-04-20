#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

from helpers import AttrDict

from console import Console
from gameconfig import GameConfig
from map import Map
from player import Player

from constants import Bind

from config import Config

CONFIG_FILE = "deityrl.json"

class DeityRL:
    def __init__(self):
        self._game_config = GameConfig.load()
        self._config = Config()
        self._worldmap = Map(self._game_config.world_width, self._game_config.world_height)
        self._output = Console()
        self._input = self._output
        self._player = Player()

        self._closed = False
    
    def has_saved_game(self):
        return False

    def load_game(self):
        raise Exception("no")

    def new_game(self):
        self._player.xy(0, 0)
        self._worldmap.generate(player=self._player)
        self._tick = 0

    def run(self):
        while not self._closed:
            map_view = self._worldmap.get_view(
                    self._player.x,
                    self._player.y,
                    self._output.get_view_width(),
                    self._output.get_view_height()
                )
            display_data = AttrDict({
                    'tick': self._tick,
                    'xy': "{}, {}".format(self._player.x, self._player.y),
                    'map_view': map_view,
                })
            self._output.render(display_data)
            key = self._input.get_key()
            self.handle_key(key)
            self.tick()

    def shutdown(self):
        self._console.teardown()

    def tick(self):
        self._tick += 1

    def handle_key(self, key):
        if key in ('q', 'Q'):
            self._closed = True
        elif key in self._config.keybindings:
            self.act_on_bound_key(key)

    def act_on_bound_key(self, key):
        binding = self._config.keybindings[key]
        if binding in (
                Bind.MOVE_N,
                Bind.MOVE_NE,
                Bind.MOVE_E,
                Bind.MOVE_SE,
                Bind.MOVE_S,
                Bind.MOVE_SW,
                Bind.MOVE_W,
                Bind.MOVE_NW
            ):
            print(binding)
            self.move_object(self._player, AttrDict({'x':binding[0], 'y':binding[1]}))

    def move_object(self, obj, movement):
        self._worldmap.move_object(obj, movement)

if __name__ == "__main__":
    out = open('out.txt', 'w')
    sys.stdout = out
    sys.stderr = out

    game = DeityRL()
    if game.has_saved_game():
        game.load_game()
    else:
        game.new_game()
    
    game.run()
