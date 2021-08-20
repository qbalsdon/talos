#!/usr/bin/env python3
import sys
from simplifier import setUp
from common import adbCommand, adbGetValue, adbSetValue, alternator, sysprops_transaction

animation_usage="""
  animation.py [-s __DEVICE__] [-t, --toggle, --on, --off]
"""
def validateArgs(arguments=None, usage=animation_usage):
    valid_args = {
        "-t" : None,
        "--toggle" : None,
        "--on" : 1.0,
        "--off" : 0.0
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

    if len(arguments) != 1:
        raise ValueError("Unknown combination\n    " + str(arguments) + "\n" + usage)

    if arguments[0] in valid_args:
        return valid_args[arguments[0]]
    raise ValueError("Unknown argument\n    " + arguments[0]+ "\n" + usage)

def modify_animations(new_value, device):
    adbSetValue("global", "window_animation_scale", new_value, device)
    adbSetValue("global", "transition_animation_scale", new_value, device)
    adbSetValue("global", "animator_duration_scale", new_value, device)
    sysprops_transaction(device) # TODO: CHECK!!

def get_animation_state(device):
    return float(adbGetValue("global", "window_animation_scale", device))

def animation_dictionary(device):
    return {
         0.0: lambda: modify_animations("0.0", device),
         1.0: lambda: modify_animations("1.0", device)
    }

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    desired_value = validateArgs(args)
    alternator(lambda: get_animation_state(device), animation_dictionary(device), desired_value)
