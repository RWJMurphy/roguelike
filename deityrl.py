#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

from helpers import AttrDict

from config import Config
from console import Console
from constants import Bind
from gameconfig import GameConfig
from map import Map
from mapmaker import MapMaker
from player import Player
import traits

CONFIG_FILE = "deityrl.json"

class DeityRL:
    def __init__(self):
        self._game_config = GameConfig
        self._config = Config()
        self._worldmap = None
        self._output = Console(self._game_config.display)
        self._input = self._output
        self._player = Player()

        self._message_buffer = []

        self._closed = False
    
    def has_saved_game(self):
        return False

    def load_game(self):
        raise Exception("no")

    def new_game(self):
        self._player.xy(
                int(self._game_config.world_width/2),
                int(self._game_config.world_height/2),
            )
        maker = MapMaker()
        self._worldmap = maker.generate(self._game_config.world_width, self._game_config.world_height)
        self._worldmap.set_message(self.add_message)

        self._worldmap.insert_objects(self._player)
        self._tick = 0

    def run(self):
        while not self._closed:
            self._worldmap.restack()
            map_view = self._worldmap.get_view(
                    self._player.x,
                    self._player.y,
                    self._output.get_view_width(),
                    self._output.get_view_height()
                )
            display_data = AttrDict({
                    'view': 'main',
                    'tick': self._tick,
                    'xy': "{}, {}".format(self._player.x, self._player.y),
                    'player_health': "{}/{}".format(self._player.max_health, self._player.health),
                    'map_view': map_view,
                    'messages': self._message_buffer[-8:],
                })
            self._output.render(display_data)
            key = self._input.get_key()
            if self.handle_key(key):
                self.tick()

    def shutdown(self):
        self._console.teardown()

    def tick(self):
        self._worldmap.tick()
        self._tick += 1

    def handle_key(self, key):
        if key in ('q', 'Q'):
            self._closed = True
            return True
        elif key in self._config.keybindings:
            return self.act_on_bound_key(key)
        else:
            self.add_message("Unbound key '{}'".format(key))
            return False

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
            return self.move_object(self._player, AttrDict({'x':binding[0], 'y':binding[1]}))
        elif binding == Bind.PICKUP:
            return self._worldmap.grab_object(self._player)
        elif binding == Bind.WAIT:
            return True

    def move_object(self, obj, movement):
        if (self._worldmap.can_move_object(obj, movement)):
            return self._worldmap.move_object(obj, movement)
        else:
            return self._worldmap.object_act_in_direction(obj, movement)

    def add_message(self, message):
        if isinstance(message, list):
            self._message_buffer.extend(message)
        else:
            self._message_buffer.append(message)

    def cleanup(self):
        self._output.cleanup()

if __name__ == "__main__":
    out = open('out.txt', 'w')
    sys.stdout = out
    sys.stderr = out

    game = DeityRL()
    if game.has_saved_game():
        game.load_game()
    else:
        game.new_game()
    
    try:
        game.run()
    except:
        raise
    finally:
        game.cleanup()
