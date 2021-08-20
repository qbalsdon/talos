#!/usr/bin/env python3
import sys
from simplifier import setUp
from common import adbCommand, adbGetValue, adbSetValue, alternator, sysprops_transaction

show_layout_usage="""
  show_layout.py [-s __DEVICE__] [-t, --toggle, --on, --off]
"""
def validateArgs(arguments=None, usage=show_layout_usage):
    valid_args = {
        "-t" : None,
        "--toggle" : None,
        "--on" : "true",
        "--off" : "false"
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

# setprop debug.layout true
def modify_show_layout(new_value, device):
    adbCommand(["shell", "setprop", "debug.layout", new_value], device)
    sysprops_transaction(device)

def get_show_layout(device):
    value = adbCommand(["shell", "getprop", "debug.layout"], device)
    if value == None or value == "":
        value = "false"
    return value

def show_layout_dictionary(device):
    return {
         "true": lambda: modify_show_layout("true", device),
         "false": lambda: modify_show_layout("false", device)
    }

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    desired_value = validateArgs(args)
    alternator(lambda: get_show_layout(device), show_layout_dictionary(device), desired_value)
