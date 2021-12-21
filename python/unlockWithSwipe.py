#!/usr/bin/env python3
import time
import sys
from simplifier import setUp
from common import adbCommand, press_button, type_text
from swipe import validateArgs, swipe_device

unlock_usage="""
  unlockWithSwipe.py [-s DEVICE] [-u|-d|-l|-r] -t [TEXT_TO_TYPE] [-e]
"""

def get_screen_settings(device):
    return adbCommand(["shell", "dumpsys", "power"], device)

def is_screen_on(device, get_settings=get_screen_settings):
    settings = get_settings(device)
    if "Display Power: state=ON" in settings:
        return True
    return False

def ensure_screen_off(device, command=lambda: press_power(device)):
    if is_screen_on(device):
        command()

def press_power(device):
    press_button("KEYCODE_POWER", device)

def unlock(options, press_enter):
    device=options.get("device")
    ensure_screen_off(device)
    screen_is_on = is_screen_on(device)
    while screen_is_on:
        press_power(device)
        time.sleep(0.5)
        screen_is_on = is_screen_on(device)

    press_power(device)
    swipe_device("u", options)
    type_text(options.get("text"), device)
    if press_enter:
        press_button("KEYCODE_ENTER", device)

if __name__ == "__main__":
    options = setUp(ui_required = False)
    args = sys.argv
    del args[0]
    press_enter = False
    if "-e" in args:
        pos = args.index("-e")
        del args[pos]
        press_enter = True

    script_args = validateArgs(args, unlock_usage)
    unlock(options, press_enter)
    # ensure_screen_off(device)
    # screen_is_on = is_screen_on(device)
    # while screen_is_on:
    #     screen_is_on = is_screen_on(device)
    # press_power(device)
    # swipe_device("u", options)
    # type_text(options.get("text"), device)
    # press_button("KEYCODE_ENTER", device)
