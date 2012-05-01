# -*- coding: utf-8 -*-
import curses
import time

__all__ = ['View', 'Console']

class View:
    def __init__(self, width, height):
        self.height = height
        self.width = width

class Console:
    def __init__(self, config):
        self._mainscreen = curses.initscr()
        curses.start_color()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        self._mainscreen.keypad(1)

        height, width = self._mainscreen.getmaxyx()
        self._map_view = self._mainscreen.subwin(
                height - config.messagebar_height,
                width - config.sidebar_width,
                0, 0
            )
        self._side_bar = self._mainscreen.subwin(
                height,
                config.sidebar_width,
                0, width - config.sidebar_width - 1
            )
        self._message_bar = self._mainscreen.subwin(
                config.messagebar_height,
                width - config.sidebar_width,
                height - config.messagebar_height - 1, 0
            )


    def __del__(self):
        self._mainscreen.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(2)
        curses.endwin()

    def cleanup(self):
        self._mainscreen.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(2)
        curses.endwin()

    def render(self, display_data):
        if display_data.view == "main":
            y = 0
            for line in display_data.map_view:
                self._map_view.addstr(y, 0, ''.join(line))
                y += 1

            self._side_bar.erase()
            self._side_bar.addstr(1, 1, "  HP: {}".format(display_data.player_health))
            self._side_bar.addstr(2, 1, "Turn: {}".format(display_data.tick))
            self._side_bar.addstr(3, 1, " Pos: {}".format(display_data.xy))

            self._message_bar.erase()
            y = 0
            for line in display_data.messages:
                self._message_bar.addstr(y, 0, line)
                y += 1

        self._side_bar.noutrefresh()
        self._message_bar.noutrefresh()
        self._map_view.noutrefresh()
        self._mainscreen.noutrefresh()

        curses.doupdate()

    def get_key(self):
        return self._mainscreen.getkey()

    def get_view_height(self):
        return self._map_view.getmaxyx()[0] - 1

    def get_view_width(self):
        return self._map_view.getmaxyx()[1] - 1

