#!/usr/bin/env python3
import sys
from simplifier import setUp
from common import adbGetValue, adbSetValue

"""
adb -s __DEVICE__  shell settings put system screen_brightness __BRIGHTNESS__
"""

brightness_usage="""
  brightness [-s device] [-p PERCENT]
"""

def get_brightness(device):
    return int(adbGetValue("system", "screen_brightness", device=device, output=True))

def set_brightness(device, brightness):
    adbSetValue("system", "screen_brightness", str(brightness), device=device, output=False)

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    if "percent" in options:
        set_brightness(device, int(options["percent"]))
    else:
        if get_brightness(device) > 0:
            set_brightness(device, 0)
        else:
            set_brightness(device, 100)
