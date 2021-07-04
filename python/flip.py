#!/usr/bin/env python3
import sys
from functools import partial
from simplifier import setUp
from common import adbSetValue, adbGetValue
from common import toggle_value
from enums import orientation

"""
adb -s __DEVICE__ shell settings put system accelerometer_rotation 0
adb -s __DEVICE__ shell settings get system user_rotation
adb -s __DEVICE__ shell settings put system user_rotation $VALUE
"""

flip_usage="""
  flip [-s DEVICE] [-t (default) | --toggle | -p | --portrait | -l | --landscape]
"""

def validateArgs(arguments=None):
    if arguments != None or len(arguments) > 0:
        if "-s" in arguments:
            pos = arguments.index("-s")
            del arguments[pos + 1]
            arguments.remove("-s")
        if len(arguments) > 1:
            raise ValueError("Illegal combination of arguments. Usage: " + flip_usage)
        if len(arguments) == 0 or "-t" in arguments or "--toggle" in arguments:
            return orientation.TOGGLE
        if "-l" in arguments or "--landscape" in arguments:
            return orientation.LANDSCAPE
        if "-p" in arguments or "--portrait" in arguments:
            return orientation.PORTRAIT
        raise ValueError("Illegal argument: " + arguments[0] + ". Usage: " + flip_usage)
    return orientation.TOGGLE

def get_orientation(device):
    return adbGetValue("system", "user_rotation", device)

def set_orientation(device, direction_int):
    adbSetValue("system", "user_rotation", str(direction_int), device)

def flip(direction, device):
    current_value = int(get_orientation(device))
    if current_value != int(direction):
        set_orientation(device, direction.convertToAndroidValue(current_value))

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    direction = validateArgs(args)
    #always required
    adbSetValue("system", "accelerometer_rotation", "0", device)
    flip(direction, device)
