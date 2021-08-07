#!/usr/bin/env python3
import sys
from functools import partial
from simplifier import setUp
from common import adbCommand, alternator
from deviceManager import getScreenSize

"""
adb -s __DEVICE__ shell settings put gloabl debug.force_rtl [0.0 | 1.0]
"""

forcertl_usage="""
  forcertl
"""

def validateArgs(arguments=None):
    if arguments == None:
        return None
    if len(arguments) > 0:
        if "-s" in arguments:
            pos = arguments.index("-s")
            del arguments[pos + 1]
            arguments.remove("-s")
        if len(arguments) == 0:
            return None
        if len(arguments) > 0:
            raise ValueError("Illegal combination of arguments. Usage: " + forcertl_usage)
    return None

def modify_forcertl(new_value, device):
    adbCommand(["shell", "setprop", "debug.force_rtl", new_value], device, False)
    # force a refresh size
    output_size = getScreenSize()
    size_string = "{}x{}".format(int(output_size["width"] / 0.99), int(output_size["height"]))
    adbCommand(["shell", "wm", "size", size_string], device, False)
    size_string = "{}x{}".format(int(output_size["width"]), int(output_size["height"]))
    adbCommand(["shell", "wm", "size", size_string], device, False)

def get_forcertl(device):
    return adbCommand(["shell", "getprop", "debug.force_rtl"], device)

def forcertl_dictionary(device):
    return {
         "false": lambda: modify_forcertl("false", device),
         "true": lambda: modify_forcertl("true", device)
    }

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    direction = validateArgs(args)
    alternator(lambda: get_forcertl(device), forcertl_dictionary(device), direction)
