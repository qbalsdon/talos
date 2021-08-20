#!/usr/bin/env python3
import sys
from functools import partial
from simplifier import setUp
from forcertl import force_refresh
from common import adbSetValue, adbGetValue, alternator, adbCommand

"""
adb shell wm density
SECURE
    display_density_forced ['', 374.0, 490.0, 540.0]
adb -s __DEVICE__ shell settings put secure display_density_forced [374.0, default, 490.0, 540.0]
"""

density_usage="""
  density [ 374.0 | default | 490.0 | 540.0 ]
"""

def validateArgs(arguments=None):
    valid_args = {
        "374" : "374",
        "440": "440",
        "490" : "490",
        "540" : "540",
        "374.0" : "374",
        "440.0": "440",
        "490.0" : "490",
        "540.0" : "540"
    }
    if arguments == None:
        return None
    if len(arguments) > 0:
        if "-s" in arguments:
            pos = arguments.index("-s")
            del arguments[pos + 1]
            arguments.remove("-s")
        if len(arguments) == 0:
            return None
        if len(arguments) > 1:
            raise ValueError("Illegal combination of arguments. Usage: " + density_usage)
        if arguments[0] not in valid_args:
            raise ValueError("Illegal argument: " + arguments[0] + ". Usage: " + density_usage)
        return valid_args[arguments[0]]
    return None

def modify_density(new_value, device):
    adbCommand(["shell", "wm", "density", new_value], device)

def get_density(device):
    value = adbGetValue("secure", "display_density_forced", device)
    if value not in density_dictionary(device):
        value = "440"
    return value

def density_dictionary(device):
    return {
         "374": lambda: modify_density("374", device),
         "440": lambda: modify_density("440", device),
         "490": lambda: modify_density("490", device),
         "540": lambda: modify_density("540", device)
    }

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    direction = validateArgs(args)
    alternator(lambda: get_density(device), density_dictionary(device), direction)
