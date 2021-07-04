#!/usr/bin/env python3

from enum import IntEnum

class orientation(IntEnum):
    PORTRAIT = 0
    LANDSCAPE = 1
    TOGGLE = 2

    def convertToAndroidValue(self, current_value):
        if current_value not in [int(orientation.PORTRAIT), int(orientation.LANDSCAPE)]:
            raise ValueError("Illegal value: " + str(current_value))
        if self == orientation.TOGGLE:
            return 1 - current_value
        return int(self)
