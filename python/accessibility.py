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
    com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService:com.balsdon.accessibilityDeveloperService/.AccessibilityDeveloperService
    com.google.android.apps.accessibility.auditor/com.google.android.apps.accessibility.auditor.ScannerService:com.android.talkback/com.google.android.marvin.talkback.TalkBackService
"""

accessibility_usage="""
  accessibility [-s device] [-t|-d|-sr|-ac] [--toggle|--disable|--screenreader|--accessibilityscanner]
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

    if len(arguments) > 1:
        raise ValueError("Cannot can only have 1 accessibility argument\n    "+accessibility_usage)

    valid_args = {
        "-t": None,
        "-d":"com.android.talkback/com.google.android.marvin.talkback.TalkBackService",
        "-sr":"com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService:com.balsdon.accessibilityDeveloperService/.AccessibilityDeveloperService",
        "-ac":"com.google.android.apps.accessibility.auditor/com.google.android.apps.accessibility.auditor.ScannerService:com.android.talkback/com.google.android.marvin.talkback.TalkBackService",
        "--toggle":None,
        "--disable":"com.android.talkback/com.google.android.marvin.talkback.TalkBackService",
        "--screenreader":"com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService:com.balsdon.accessibilityDeveloperService/.AccessibilityDeveloperService",
        "--accessibilityscanner":"com.google.android.apps.accessibility.auditor/com.google.android.apps.accessibility.auditor.ScannerService:com.android.talkback/com.google.android.marvin.talkback.TalkBackService"
    }
    if arguments[0] not in valid_args:
        raise ValueError("Argument '" + arguments[0] + " not recognised'\n    "+accessibility_usage)
    return valid_args[arguments[0]]

def get_accessibility_state(device):
    # adv shell settings get secure enabled_accessibility_services
    return adbGetValue("secure", "enabled_accessibility_services", device)

def turn_off(device):
    adbSetValue("secure", "enabled_accessibility_services", "com.android.talkback/com.google.android.marvin.talkback.TalkBackService", device)
    adbSetValue("secure", "accessibility_enabled", "0", device)

def turn_on_defaults(device):
    adbSetValue("secure", "accessibility_enabled", "0", device)

def turn_on_screen_reader(device):
    turn_on_defaults(device)
    adbSetValue("secure", "enabled_accessibility_services", "com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService:com.balsdon.accessibilityDeveloperService/.AccessibilityDeveloperService", device)

def turn_on_scanner(device):
    turn_on_defaults(device)
    adbSetValue("secure", "enabled_accessibility_services", "com.google.android.apps.accessibility.auditor/com.google.android.apps.accessibility.auditor.ScannerService:com.android.talkback/com.google.android.marvin.talkback.TalkBackService", device)

def accessibility_dictionary(device):
    return {
         "com.android.talkback/com.google.android.marvin.talkback.TalkBackService": lambda: turn_off(device),
         "com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService:com.balsdon.accessibilityDeveloperService/.AccessibilityDeveloperService": lambda: turn_on_screen_reader(device),
         "com.google.android.apps.accessibility.auditor/com.google.android.apps.accessibility.auditor.ScannerService:com.android.talkback/com.google.android.marvin.talkback.TalkBackService" : lambda: turn_on_scanner(device)
    }

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    args = sys.argv
    del args[0]
    service = validateArgs(args)
    alternator(lambda: get_accessibility_state(device), accessibility_dictionary(device), service)
