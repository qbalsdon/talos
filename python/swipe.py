#!/usr/bin/env python3
import sys
from functools import partial
from simplifier import setUp
from common import adbCommand
from deviceManager import getScreenSize

swipe_usage = "swipe [-s DEVICE] [-u|-d|-l|-r] [-p PERCENT]"

def validateArgs(arguments=None):
    DEFAULT_RETURN = "u"
    if arguments == None:
        return DEFAULT_RETURN
    if len(arguments) > 0:
        if "-s" in arguments:
            pos = arguments.index("-s")
            del arguments[pos + 1]
            arguments.remove("-s")
        if "-p" in arguments:
            pos = arguments.index("-p")
            del arguments[pos + 1]
            arguments.remove("-p")

    if len(arguments) == 0:
        return DEFAULT_RETURN

    if len(arguments) > 1:
        raise ValueError("Can only have 1 argument\n    " + swipe_usage)

    valid_args = {
        "-u": "u",
        "-d": "d",
        "-l": "l",
        "-r": "r"
    }

    if arguments[0] not in valid_args:
        raise ValueError("Argument '" + arguments[0] + " not recognised'\n    " + swipe_usage)
    return valid_args[arguments[0]]

def percent_length(length, percent):
    return int(length * percent / 100)

def determine_swipe_points(screen_size, direction, percent):
    if percent < 0:
        percent = 0
    if percent > 100:
        percent  = 100
    centerX = screen_size["width"] / 2
    centerY = screen_size["height"] / 2

    if direction in ["l" ,"r"]:
        offset = (screen_size["width"] * percent / 100) / 2

        if direction == "l":
            return int(centerX + offset), int(centerY), int(centerX - offset), int(centerY)
        return int(centerX - offset), int(centerY), int(centerX + offset), int(centerY)

    if direction in ["u", "d"]:
        offset = (screen_size["height"] * percent / 100) / 2
        if direction == "u":
            return int(centerX), int(centerY + offset), int(centerX), int(centerY - offset)
        return int(centerX), int(centerY - offset), int(centerX), int(centerY + offset)

def perform_swipe(startX, startY, endX, endY, device):
    adbCommand(["shell", "input", "swipe", str(startX), str(startY), str(endX), str(endY)], device)

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]

    direction = validateArgs(args)
    screen_size = getScreenSize(options = options)
    percent = 50
    if "percent" in options:
        percent = int(options["percent"])

    print("I am going to swipe {} {}% on {}".format(direction, percent, screen_size))
    x1, x2, y1, y2 = determine_swipe_points(screen_size, direction, percent)
    perform_swipe(x1, x2, y1, y2, device)
