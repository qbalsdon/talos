#!/usr/bin/env python3
import sys
from functools import partial
from simplifier import setUp
from common import adbSetValue, adbGetValue, alternator

"""
adb -s __DEVICE__ shell settings put system font_scale __SCALE__
"""

fontscale_usage="""
  font_scale [ -t --toggle -sm --small -d --default -l --large -el --largest ]
"""

def validateArgs(arguments=None):
    valid_args = {
        "-t" : None,
        "--toggle" : None,
        "-sm" : 0.85,
        "-small" : 0.85,
        "-d" : 1,
        "--default" : 1,
        "-l" : 1.15,
        "--large" : 1.15,
        "-el" : 1.3,
        "--largest" : 1.3
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
            raise ValueError("Illegal combination of arguments. Usage: " + fontscale_usage)
        if arguments[0] not in valid_args:
            raise ValueError("Illegal argument: " + arguments[0] + ". Usage: " + fontscale_usage)
        return valid_args[arguments[0]]
    return None

def modify_font_scale(new_value, device):
    adbSetValue("system", "font_scale", new_value, device)

def get_font_scale(device):
    return float(adbGetValue("system", "font_scale", device))

def font_scale_dictionary(device):
    return {
         0.85: lambda: modify_font_scale("0.85", device),
         1.0:  lambda: modify_font_scale("1.0", device),
         1.15: lambda: modify_font_scale("1.15", device),
         1.13: lambda: modify_font_scale("1.13", device)
    }

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    direction = validateArgs(args)
    alternator(lambda: get_font_scale(device), font_scale_dictionary(device), direction)
