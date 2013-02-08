# -*- coding: utf-8 -*-
from constants import Bind

__all__ = ['Config']

class Config:
    keybindings = {
        'KEY_UP': Bind.MOVE_N,
        'KEY_RIGHT': Bind.MOVE_E,
        'KEY_DOWN': Bind.MOVE_S,
        'KEY_LEFT': Bind.MOVE_W,
        'h': Bind.MOVE_W,
        'j': Bind.MOVE_S,
        'k': Bind.MOVE_N,
        'l': Bind.MOVE_E,
        'y': Bind.MOVE_NW,
        'u': Bind.MOVE_NE,
        'b': Bind.MOVE_SW,
        'n': Bind.MOVE_SE,
    }
