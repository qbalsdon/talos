#!/usr/bin/env python3
from simplifier import setUp
from common import adbCommand

import re

"""
adb shell dumpsys window displays

example output:
    ...
    mCurrentFocus=Window{5fb753e u0 com.android.vending/com.android.vending.AssetBrowserActivity}
    ...
"""

currentactivity_usage="""
  currentactivity.py [-s __DEVICE__]
"""

def extract_activity(data):
    currentWindow = re.search("mCurrentFocus=.*\{.*\}", data)
    if currentWindow == None:
        return "UNKNOWN"
    return currentWindow.group().replace("{","").replace("}","").split(" ")[2]

def current_activity_name(device):
    return extract_activity(adbCommand(["shell",  "dumpsys",  "window", "displays"], device))

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    print(current_activity_name(device))
