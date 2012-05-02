# -*- coding: utf-8 -*-
import curses
import time

from color import Color

__all__ = ['View', 'Console']

class View:
    def __init__(self, width, height):
        self.height = height
        self.width = width

class Console:
    curses_colors = [
            curses.COLOR_BLACK,
            curses.COLOR_BLUE,
            curses.COLOR_CYAN,
            curses.COLOR_GREEN,
            curses.COLOR_MAGENTA,
            curses.COLOR_RED,
            curses.COLOR_WHITE,
            curses.COLOR_YELLOW,
            ]

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

        self.init_color_map()
        self._curses_color_cache = {}

    def __del__(self):
        self._mainscreen.keypad(0)
        curses.nocbreak()
        curses.echo()
        curses.curs_set(2)
        curses.endwin()

    def init_color_map(self):
        self._curses_color_map = {}
        for color_number in Console.curses_colors:
            r, g, b = curses.color_content(color_number)
            r = r * 255.0 / 1000
            g = g * 255.0 / 1000
            b = b * 255.0 / 1000
            color = Color(r, g, b)
            self._curses_color_map[color_number] = color
            curses.init_pair(color_number+1, color_number, curses.COLOR_BLACK)

    def nearest_curses_color(self, color):
        if color in self._curses_color_cache:
            return self._curses_color_cache[color]

        print("Finding nearest color to {}".format(color.rgb()))

        min_distance = None
        best_color = None
        for curses_color in Console.curses_colors:
            distance = color.distance(self._curses_color_map[curses_color])
            print("\tdistance from {} is {}".format(curses.color_content(curses_color), distance))
            if min_distance is None or distance < min_distance:
                best_color = curses_color
                min_distance = distance
            if distance == 0:
                break

        print("Got {}".format(curses.color_content(best_color)))

        self._curses_color_cache[color] = best_color
        return best_color

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
                x = 0
                for tile in line:
                    curses_color = self.nearest_curses_color(tile.color)
                    bg = curses.COLOR_BLACK

                    self._map_view.addch(
                            y, x, 
                            tile.char, 
                            curses.color_pair(self.nearest_curses_color(tile.color)+1)
                        )
                    x += 1
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
    


