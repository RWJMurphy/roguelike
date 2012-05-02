# -*- coding: utf-8 -*-

__all__ = ['Color']

class Color:
    def __init__(self, r, g, b):
        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))
        self.__r = r
        self.__g = g
        self.__b = b

    def __eq__(self, other):
        return self.rgb() == other.rgb()

    def __ne__(self, other):
        return self.rgb() != other.rgb()

    def rgb(self):
        return (self.__r, self.__g, self.__b)

    def __hash__(self):
        return self.__r * 256 * 256 + self.__g * 256 + self.__b

    def __mul__(self, other):
        r1, g1, b1 = self.rgb()
        if isinstance(other, Color):
            r2, g2, b2 = other.rgb()
            r3 = r1 * r2 / 255
            g3 = g1 * g2 / 255
            b3 = b1 * b2 / 255
        elif isinstance(other, float) or isinstance(other, int):
            r3 = max(0, min(r1 * other, 255))
            g3 = max(0, min(g1 * other, 255))
            b3 = max(0, min(b1 * other, 255))
        else:
            return NotImplemented
        return Color(r3, g3, b3)

    def __add__(self, other):
        r1, g1, b1 = self.rgb()
        if isinstance(other, Color):
            r2, g2, b2 = other.rgb()
            r3 = min(255, r1 + r2)
            g3 = min(255, g1 + g2)
            b3 = min(255, b1 + b2)
        else:
            return NotImplemented
        return Color(r3, g3, b3)

    def __sub__(self, other):
        r1, g1, b1 = self.rgb()
        if isinstance(other, Color):
            r2, g2, b2 = other.rgb()
            r3 = max(0, r1 - r2)
            g3 = max(0, g1 - g2)
            b3 = max(0, b1 - b2)
        else:
            return NotImplemented
        return Color(r3, g3, b3)

    def distance(self, other):
        r1, g1, b1 = self.rgb()
        r2, g2, b2 = other.rgb()

        return sum([
                abs(r1 - r2),
                abs(g1 - g2),
                abs(b1 - b2)
        ])

    @staticmethod
    def from_hsv(hue, saturation, value):
        if not 0 < hue < 360:
            raise ValueError("hue out of range")
        if not 0 < saturation < 1:
            raise ValueError("saturation out of range")
        if not 0 < value < 1:
            raise ValueError("value out of range")

        chroma = hue * saturation
        hue_ = hue / 60.0
        x = chroma * (1 - abs(hue_ % 2 - 1))

        if hue_ < 1:
            red_, green_, blue_ = (chroma, x, 0)
        elif hue_ < 2:
            red_, green_, blue_ = (x, chroma, 0)
        elif hue_ < 3:
            red_, green_, blue_ = (0, chroma, x)
        elif hue_ < 4:
            red_, green_, blue_ = (0, x, chroma)
        elif hue_ < 5:
            red_, green_, blue_ = (x, 0, chroma)
        elif hue_ < 6:
            red_, green_, blue_ = (chroma, 0, x)

        m = value - chroma
        red, green, blue = red_ + m, green_ + m, blue_ + m
        return Colr(red, green, blue)
