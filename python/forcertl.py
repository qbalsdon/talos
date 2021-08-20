#!/usr/bin/env python3
import sys
from functools import partial
from simplifier import setUp, parseXML
from common import adbCommand, alternator, adbSetValue, adbGetValue, press_button
from deviceManager import getScreenSize
from openscreen import getOption
from tap import tap_element
"""
adb -s __DEVICE__ shell settings put global debug.force_rtl [0.0 | 1.0]
adb shell settings put gloabl debug.force_rtl 0.0
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

def force_refresh(device):
    # force a refresh size
    # ----RATTLE----
    # output_size = getScreenSize(device = device)
    # size_string = "{}x{}".format(int(output_size["width"] / 0.59), int(output_size["height"]))
    # adbCommand(["shell", "wm", "size", size_string], device, False)
    # size_string = "{}x{}".format(int(output_size["width"]), int(output_size["height"]))
    # adbCommand(["shell", "wm", "size", "reset"], device, False)
    # -------------
    # adbCommand(["adb", "shell", "settings", "put", "system", "user_rotation", "3"], device) # landscape
    # adbCommand(["adb", "shell", "settings", "put", "system", "user_rotation", "0"], device) # portrait
    adbCommand(getOption("locale"), device)
    options = {"element":"dragHandle", "device":device}
    tap_element(options, parseXML(options=options))
    press_button("KEYCODE_BACK", device)

def modify_forcertl(new_value, device):
    # adb shell settings put global debug.force_rtl 1.0
    adbSetValue("global", "debug.force_rtl", new_value, device)
    prop_value = "false"
    if new_value != "0":
        prop_value = "true"

    adbCommand(["shell", "setprop", "debug.force_rtl", prop_value], device, False)
    # print("SET\nProp value:   [{}]\nGlobal value: [{}]".format(prop_value, new_value))
    force_refresh(device)

def get_forcertl(device):
    prop_value = adbCommand(["shell", "getprop", "debug.force_rtl"], device)
    global_value = str(adbGetValue("global", "debug.force_rtl", device))
    global_value = global_value.replace(".0", "")
    # print("GET\nProp value:   [{}]\nGlobal value: [{}]".format(prop_value, global_value))
    return global_value


def forcertl_dictionary(device):
    return {
         "1": lambda: modify_forcertl("1", device),
         "0": lambda: modify_forcertl("0", device)
    }

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    direction = validateArgs(args)
    alternator(lambda: get_forcertl(device), forcertl_dictionary(device), direction)
