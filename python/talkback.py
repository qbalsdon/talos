#!/usr/bin/env python3
import sys
from functools import partial
from simplifier import setUp
from common import adbSetValue, adbGetValue, alternator

"""
ALWAYS:
    adb -s "$DEVICE" shell settings put secure accessibility_enabled [1=ON|0=OFF]
SETTINGS:
    adb -s "$DEVICE" shell am start -n com.google.android.marvin.talkback/com.android.talkback.TalkBackPreferencesActivity

VALUE_OFF:
    com.android.talkback/com.google.android.marvin.talkback.TalkBackService

ACCESSIBILITY SERVICES:
    com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService
    com.balsdon.accessibilityDeveloperService/.AccessibilityDeveloperService

"""

talkback_usage="""
  talkback [-s device] [-t|-d|-m|-sr|-ac] [--toggle|--disable|--menu|--screenreader|--accessibilityscanner]
"""

def validateArgs(arguments=None):
    # if arguments == None:
    #     return None
    # if len(arguments) > 0:
    #     if "-s" in arguments:
    #         pos = arguments.index("-s")
    #         del arguments[pos + 1]
    #         arguments.remove("-s")
    #     if len(arguments) > 1:
    #         raise ValueError("Illegal combination of arguments. Usage: " + flip_usage)
    #     if len(arguments) == 0 or "-t" in arguments or "--toggle" in arguments:
    #         return None
    #     if "-l" in arguments or "--landscape" in arguments:
    #         return 0
    #     if "-p" in arguments or "--portrait" in arguments:
    #         return 1
    #     raise ValueError("Illegal argument: " + arguments[0] + ". Usage: " + flip_usage)
    return None

def modifier(str):
    # adbSetValue("system", "user_rotation", str, device)

def get_service(device):
    # return int(adbGetValue("system", "user_rotation", device))

def talkback_dictionary(device):
    pass
    # return {
    #      0: lambda: modifier("1"), #change from LANDSCAPE to PORTRAIT
    #      1: lambda: modifier("0")  #change from PORTRAIT to LANDSCAPE
    # }

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    direction = validateArgs(args)
    #always required
    # adbSetValue("system", "accelerometer_rotation", "0", device)

    # alternator(lambda: get_orientation(device), flip_dictionary(device), direction)
