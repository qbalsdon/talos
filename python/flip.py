#!/usr/bin/env python3
import sys
from functools import partial
from simplifier import setUp
from common import adbSetValue, adbGetValue, alternator

"""
adb -s __DEVICE__ shell settings put system accelerometer_rotation 0
adb -s __DEVICE__ shell settings get system user_rotation
adb -s __DEVICE__ shell settings put system user_rotation $VALUE
"""

flip_usage="""
  flip [-s DEVICE] [-t (default) | --toggle | -p | --portrait | -l | --landscape]
"""

def validateArgs(arguments=None):
    if arguments == None:
        return None
    if len(arguments) > 0:
        if "-s" in arguments:
            pos = arguments.index("-s")
            del arguments[pos + 1]
            arguments.remove("-s")
        if len(arguments) > 1:
            raise ValueError("Illegal combination of arguments. Usage: " + flip_usage)
        if len(arguments) == 0 or "-t" in arguments or "--toggle" in arguments:
            return None
        if "-l" in arguments or "--landscape" in arguments:
            return 1
        if "-p" in arguments or "--portrait" in arguments:
            return 0
        raise ValueError("Illegal argument: " + arguments[0] + ". Usage: " + flip_usage)
    return None

def modifier(new_value):
    adbSetValue("system", "user_rotation", new_value, device)

def get_orientation(device):
    return int(adbGetValue("system", "user_rotation", device))

def flip_dictionary(device):
    return {
         0: lambda: modifier("0"), #change from LANDSCAPE to PORTRAIT
         1: lambda: modifier("1")  #change from PORTRAIT to LANDSCAPE
    }

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    direction = validateArgs(args)
    #always required
    adbSetValue("system", "accelerometer_rotation", "0", device)

    alternator(lambda: get_orientation(device), flip_dictionary(device), direction)
