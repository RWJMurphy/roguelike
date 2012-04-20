# -*- coding: utf-8 -*-
import curses
import time

class View:
    def __init__(self, width, height):
        self.height = height
        self.width = width

class Console:
    def __init__(self):
        self._map_view = View(80, 25)
        self._mainscreen = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        self._mainscreen.keypad(1)

    def __del__(self):
        self._mainscreen.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(2)
        curses.endwin()

    def render(self, display_data):
        y = 0
        for line in display_data.map_view:
            self._mainscreen.addstr(y, 0, ''.join(line))
            y += 1
        self._mainscreen.addstr(y, 0, "Turn:{} Pos:{}          ".format(display_data.tick, display_data.xy))
        self._mainscreen.refresh()

    def get_key(self):
        return self._mainscreen.getkey()

    def get_view_height(self):
        return self._map_view.height

    def get_view_width(self):
        return self._map_view.width

