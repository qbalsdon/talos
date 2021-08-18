#!/usr/bin/env python3
import sys
from simplifier import setUp, parseXML
from common import adbCommand, adbGetValue, press_button
from openscreen import getOption
from tap import tap_element

darkMode_usage="""
  darkMode.py [-s __DEVICE__] [-t, --toggle, -d, --dark, -l, --light]
"""
def validateArgs(arguments=None):
    valid_args = {
        "-t" : None,
        "--toggle" : None,
        "-d" : "dark",
        "--dark" : "dark",
        "-l" : "light",
        "--light" : "light"
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
        raise ValueError("Unknown combination\n    " + str(arguments) + "\n" + darkMode_usage)

    if arguments[0] in valid_args:
        return valid_args[arguments[0]]
    raise ValueError("Unknown argument\n    " + arguments[0]+ "\n" + darkMode_usage)


def get_state(device):
    # ui_night_mode [1.0, 2.0]
    night_mode = adbGetValue("secure", "ui_night_mode", device=device, output=True)
    return int(night_mode)

def change_required(device, argument, read_state=get_state):
    if argument == None:
        return True
    if argument not in ["dark","light"]:
        raise ValueError("Unknown parameter: " + argument)
    state = read_state(device)
    return (state == 1 and argument == "dark") or (state == 2 and argument == "light")


if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]

    argument = validateArgs(args)

    changeRequired = change_required(device, argument)

    if changeRequired:
        adbCommand(getOption("display"), device)
        uiRoot = parseXML(options = options)
        options["element"] = "switchWidget"
        tap_element(options, uiRoot)
        press_button("KEYCODE_BACK", device)
