# -*- coding: utf-8 -*-
from constants import Bind

__all__ = ['Config']

class Config:
    keybindings = {
        'KEY_UP': Bind.MOVE_N,
        'KEY_RIGHT': Bind.MOVE_E,
        'KEY_DOWN': Bind.MOVE_S,
        'KEY_LEFT': Bind.MOVE_W,
    }
