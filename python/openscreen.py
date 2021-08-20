#!/usr/bin/env python3
import sys
from simplifier import setUp
from common import adbCommand

openscreen_usage="""
  openscreen.py [-s __DEVICE__] -n NAME
"""

def validateArgs(arguments=None):
    if arguments == None:
        raise ValueError("1 argument required\n    " + openscreen_usage)
    if len(arguments) > 0:
        if "-s" in arguments:
            pos = arguments.index("-s")
            del arguments[pos + 1]
            arguments.remove("-s")
    if len(arguments) != 1:
        raise ValueError("1 argument required\n    " + openscreen_usage)
    if arguments[0] in screen_options or arguments[0] in activity_screens:
        return arguments[0]
    raise ValueError("Unknown argument\n    " + arguments[0])

# https://stackoverflow.com/a/68655882/932052
screen_options={
    "developer":"com.android.settings.APPLICATION_DEVELOPMENT_SETTINGS",
    "dark": "android.settings.DARK_THEME_SETTINGS",
    "colour_inversion": "com.android.settings.ACCESSIBILITY_COLOR_SPACE_SETTINGS",
    "display": "android.settings.DISPLAY_SETTINGS",
    "bluetooth": "android.settings.BLUETOOTH_SETTINGS",
    "wifi":"android.settings.WIFI_SETTINGS",
    "airplane": "android.settings.AIRPLANE_MODE_SETTINGS",
    "accessibility":"android.settings.ACCESSIBILITY_SETTINGS",
    "locale": "android.settings.LOCALE_SETTINGS",
}

activity_screens={
    "talkback":"com.google.android.marvin.talkback/com.android.talkback.TalkBackPreferencesActivity",
    # "talkback_dev": "com.google.android.marvin.talkback/com.google.android.accessibility.talkback.TalkBackDeveloperPreferencesActivity",
}

def getOption(option):
    if option in screen_options:
        return ["shell", "am", "start", "-a", screen_options[option]]
    if option in activity_screens:
        return ["shell", "am", "start", "-n", activity_screens[option]]

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    adbCommand(getOption(validateArgs(args)), device)
