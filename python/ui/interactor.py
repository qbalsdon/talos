#!/usr/bin/env python3
import subprocess
import sys
import os
import json
from datetime import date

sys.path.append('../../python')
from unlockWithSwipe import *
from darkMode import *
from common import alternator, adbSetValue
from forcertl import get_forcertl, forcertl_dictionary
from accessibility import turn_on_accessibility_service
from fontscale import toggle_font_scale, modify_font_scale
from currentactivity import current_activity_name
from openscreen import screen_options, open_activity
from simplifier import fetchDeviceRawData

def run_on_all_selected_devices(fn, device_list):
    list = device_list
    if (len(list) > 0):
        fn(list)

def get_focus_app():
    return read_settings_file('FOCUS_APP_PACKAGE')

def read_settings_file(settings):
    file_location = os.environ['TALOS_SETTINGS']
    with open(file_location, 'r') as file:
        data = file.read()
    return json.loads(data)[settings]

def get_system_data(setting_section):
    return read_settings_file(setting_section)

def get_device_details(device_serial, key, default):
    names = get_system_data('DEVICE_NAMES')
    if device_serial in names:
        return names[device_serial][key]
    else:
        return default

def get_device_name(device_serial):
    name = get_device_details(device_serial, "name", "")
    if name == "":
        return None
    else:
        return name

def run_command_async(commands):
    subprocess.Popen(commands, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def run_command(commands):
    subprocess.run(commands, capture_output=False)

def run_command_return(commands):
    value = subprocess.run(commands, stdout=subprocess.PIPE).stdout.decode().strip()
    return value

def run_adb_command(device, commands):
    command_list = ["adb","-s", device] + commands
    run_command(command_list)

def run_adb_command_return(device, commands):
    command_list = ["adb","-s", device] + commands
    return run_command_return(command_list)

def adb_type_text(device, string):
    run_adb_command(device, ["shell", "input", "text", string.replace(" ","%s")])

def adb_type_key_code(device, key_code):
    run_adb_command(device, ["shell", "input", "keyevent", key_code])

def adb_tap_pos(device, x, y):
    run_adb_command(device, ["shell", "input", "tap", f"{x}", f"{y}"])

def adb_reboot(device):
    run_adb_command(device, ["reboot"])

def clear_cache(device, package_name):
    run_adb_command(device, ["shell", "pm", "clear", package_name])

def run_activity(device, package_name, activity_name):
    run_adb_command(device, ["shell", "am", "start", "-n", f"\"{package_name}/{package_name}.{activity_name}\"", "-a", "android.intent.action.MAIN", "-c", "android.intent.category.LAUNCHER"])

def open_screen(device, name):
    run_adb_command(device, ["shell", "am", "start", "-a", name])

def enter_login_details(device, username, password):
    # adb_type_text(device, "milan.vidic@zuehlke.com")
    adb_type_text(device, username)
    adb_type_key_code(device, "KEYCODE_TAB")
    # adb_type_text(device, "gcZB5X4MU7PenKPPWj4zaPzep")
    adb_type_text(device, password)
    adb_type_key_code(device, "KEYCODE_ENTER")

def screen_brightness(device, value):
    run_adb_command(device, ["shell", "settings", "put", "system", "screen_brightness", f"{value}"])

def screen_timeout(device, millis):
    run_adb_command(device, ["shell", "settings", "put", "system", "screen_off_timeout", f"{millis}"])

def set_language(device, language):
    run_adb_command(device, ["shell", f"setprop persist.sys.language {language}; setprop persist.sys.country UK; setprop ctl.restart zygote"])

def open_app_settings(device):
    run_adb_command(device, ["shell", "am", "broadcast", "-a", "tigerbox.action.settings"])

def app_no_update(device):
    run_adb_command(device, ["shell", "am", "broadcast", "-a", "tigerbox.action.config.set", "-e", "software.version.date", "2051-01-01T00:00:00.000+0000"])

def get_device_list():
    return subprocess.run(["adb","devices"], capture_output=True).stdout.decode().strip().split('\n', 1)[-1]

def loop_command(device_list, fn):
    for device in device_list:
        fn(device)

def loop_command_return_process(device_list, fn, post_process):
    ret = {}
    for device in device_list:
        device_value = fn(device)
        # print(f"\n    --> {device}: [{device_value}]\n\n")
        ret[device] = post_process(device_value)
    return ret

def loop_command_return(device_list, fn):
    ret = {}
    for device in device_list:
        ret[device] = fn(device)
    return ret


def device_get_info(device_list, package_name, filter):
    # adb -s $DEV shell dumpsys package media.tiger.tigerbox | grep versionCode
    return loop_command_return_process(
        device_list,
        lambda device: run_adb_command_return(device, ["shell", "dumpsys", "package", package_name, "|", "grep", filter]),
        lambda value: value.replace("\r\n"," - ")
    )

def device_get_system_property_info(device_list, filter):
    # adb -s $DEV shell getprop | grep ro.build.display.id
    value = loop_command_return_process(
        device_list,
        lambda device: run_adb_command_return(device, ["shell", "getprop", "|", "grep", filter]),
        lambda value: value.replace(f"[{filter}]: ", "").replace("[", "").replace("]","")
    )
    return value

def device_unlock(device_list):
    loop_command(device_list, lambda device: unlock({"device":device, "text":"314159"}, True))

def device_back(device_list):
    loop_command(device_list, lambda device: adb_type_key_code(device, "KEYCODE_BACK"))

def device_home(device_list):
    loop_command(device_list, lambda device: adb_type_key_code(device, "KEYCODE_HOME"))

def device_power(device_list):
    loop_command(device_list, lambda device: adb_type_key_code(device, "KEYCODE_POWER"))

def device_tap(device_list, x, y):
    loop_command(device_list, lambda device: adb_tap_pos(device, x, y))

def device_reboot(device_list):
    loop_command(device_list, lambda device: adb_reboot(device))

def device_clear_cache(device_list, package_name):
    loop_command(device_list, lambda device: clear_cache(device, package_name))

def show_activity(device_list, package_name, activity_name):
    loop_command(device_list, lambda device: run_activity(device, package_name, activity_name))

def device_open_screen(device_list, activity_name):
    loop_command(device_list, lambda device: open_screen(device, activity_name))

def device_set_language(device_list, language_code):
    loop_command(device_list, lambda device: set_language(device, language_code))

def get_device_details(device_serial, key, default):
    names_file_location = os.environ['DEVICE_NAMES']
    with open(names_file_location, 'r') as file:
        data = file.read()
    names = json.loads(data)
    if device_serial in names:
        return names[device_serial][key]
    else:
        return default

def get_device_name_only(device_serial):
    name = get_device_details(device_serial, "name", "")
    if name == "":
        return device_serial
    else:
        return name

def get_device_name(device_serial):
    name = get_device_details(device_serial, "name", "")
    if name == "":
        return None
    else:
        return name

def get_device_scrpcpy_options(device_serial):
    return get_device_details(device_serial, "scrcpy", "")

def scrcpy(device):
    device_friendly_name = get_device_name(device)
    if device_friendly_name == None:
        device_friendly_name = device

    device_scrcpy_option = get_device_scrpcpy_options(device)
    if device_scrcpy_option == "":
        run_command_async(["scrcpy", "-s", device, "--window-title", device_friendly_name])
    else:
        run_command_async(["scrcpy", "-s", device, "--window-title", device_friendly_name, device_scrcpy_option])

def device_scrcpy(device_list):
    loop_command(device_list, lambda device: scrcpy(device))

def start_recording(device):
    datestr=date.today().strftime("%d_%B_%Y")
    name = f"/Users/quba/Sandbox/{device}-{get_device_name_only(device).replace(' ','_')}-{datestr}.mp4"
    # name = f"/Users/quba/Downloads/recording.mp4"
    title = f"RECORDING {get_device_name(device)}"
    run_command_async(["scrcpy", "-s", device, "--record", name, "--window-title", title])


def onboarding_no_update(device, wifi_name, wifi_password, user_name, user_password):
    # .//Users/quba/repo/tigerBox/qa_scripts/onboarding_no_update.sh -s KXaPH1dhGlks32qnR2vp6v -w "FD43 Hyperoptic 1Gb Fibre 2.4Ghz" -p frRFNJP9gKRe
    script="/Users/quba/repo/tigerBox/qa_scripts/onboarding_no_update.sh"
    run_command_async([script, "-s", device, "-w", wifi_name, "-p", wifi_password, "-un", user_name, "-up", user_password])

def device_onboarding_flow(device_list, wifi_name, wifi_password, user_name, user_password):
    loop_command(device_list, lambda device: onboarding_no_update(device, wifi_name, wifi_password, user_name, user_password))

def device_record(device_list):
    loop_command(device_list, lambda device: start_recording(device))

def device_type(device_list, text):
    loop_command(device_list, lambda device: adb_type_text(device, text))

def device_sound_down(device_list):
    loop_command(device_list, lambda device: run_adb_command(device, ["shell", "service", "call", "audio", "4", "i32", "3", "i32", "7"]))

def device_clear_qa_settings(device_list):
    loop_command(device_list, lambda device: run_adb_command(device, ["shell", "am", "broadcast", "-a", "tigerbox.action.config.clear"]))

def device_reboot(device_list):
    loop_command(device_list, lambda device: run_adb_command(device, ["reboot"]))

def device_enter_login_details(device_list, username, password):
    loop_command(device_list, lambda device: enter_login_details(device, username, password))

def device_screen_brightness(device_list, value):
    loop_command(device_list, lambda device: screen_brightness(device, value))

def device_screen_timeout(device_list, millis):
    loop_command(device_list, lambda device: screen_timeout(device, millis))

def device_update(device_list, file_name):
    # adb -s $DEV push ~/Sandbox/rk312x-ota-R10.0-BTS84-20220131.073620.zip /sdcard/update.zip;
    # adb -s $DEV shell am broadcast -a "com.android.bts84.otaupgrade"
    loop_command(device_list, lambda device: run_adb_command(device, ["push", file_name, "/sdcard/update.zip"]))
    loop_command(device_list, lambda device: run_adb_command(device, ["shell", "am", "broadcast", "-a", "com.android.bts84.otaupgrade"]))

def device_open_app_settings(device_list):
    loop_command(device_list, lambda device: open_app_settings(device))
def device_app_no_update(device_list):
    loop_command(device_list, lambda device: app_no_update(device))
def device_dark_mode_toggle(device_list):
    loop_command(device_list, lambda device: dark_mode(device, None ,None))

def force_rtl(device):
    alternator(lambda: get_forcertl(device), forcertl_dictionary(device), None)

def device_force_rtl(device_list):
    # alternator(lambda: get_forcertl(device), forcertl_dictionary(device), direction)
    loop_command(device_list, lambda device: force_rtl(device))

def device_turn_on_accessibility_service(device_list, service):
    service_shortcut = {
        "disable":"com.android.talkback/com.google.android.marvin.talkback.TalkBackService",
        "screenreader":"com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService:com.balsdon.accessibilityDeveloperService/.AccessibilityDeveloperService",
        "accessibilityscanner":"com.google.android.apps.accessibility.auditor/com.google.android.apps.accessibility.auditor.ScannerService:com.android.talkback/com.google.android.marvin.talkback.TalkBackService"
    }
    action = service
    if service in service_shortcut:
        action = service_shortcut[service]

    loop_command(device_list, lambda device, param=action: turn_on_accessibility_service(device, param))

def device_accessibility_action(device_list, action, params):
    # adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_SWIPE_LEFT"
    command_params = ["shell", "am", "broadcast", "-a", "com.balsdon.talkback.accessibility", "-e", "ACTION", action]
    command_params = command_params + params
    loop_command(device_list, lambda device: run_adb_command(device, command_params))

def device_font_scale(device_list, size):
    if size == None:
        loop_command(device_list, lambda device: toggle_font_scale(device, None))
    else:
        loop_command(device_list, lambda device, param=size: modify_font_scale(param, device))

def get_current_activity_name(device_list):
    return loop_command_return(device_list, current_activity_name)

def device_open_activity(device_list, screen):
    loop_command(device_list, lambda device: open_activity(device, screen))

def set_language(device, language_code, country_code):
    # com.balsdon.accessibilityDeveloperService/.AccessibilityDeveloperService
    current_services = adbGetValue("secure", "enabled_accessibility_services", device)
    adbSetValue("secure", "accessibility_enabled", "0", device)
    adbSetValue("secure", "enabled_accessibility_services", "com.balsdon.accessibilityDeveloperService/.AccessibilityDeveloperService", device)
    run_adb_command(device, ["shell", "am", "broadcast", "-a", "com.balsdon.talkback.accessibility", "-e", "ACTION", "ACTION_SET_LANGUAGE", "-e", "PARAMETER_COUNTRY", language_code, "-e", "PARAMETER_LANGUAGE", country_code])
    adbSetValue("secure", "enabled_accessibility_services", current_services, device)

def device_set_language(device_list, language_code, country_code):
    loop_command(device_list, lambda device: set_language(device, language_code, country_code))

def device_get_ui(device_list):
    return loop_command_return(device_list, lambda device: fetchDeviceRawData({"device":device}))
# 0 -->  "KEYCODE_UNKNOWN"
# 1 -->  "KEYCODE_MENU"
# 2 -->  "KEYCODE_SOFT_RIGHT"
# 3 -->  "KEYCODE_HOME"
# 4 -->  "KEYCODE_BACK"
# 5 -->  "KEYCODE_CALL"
# 6 -->  "KEYCODE_ENDCALL"
# 7 -->  "KEYCODE_0"
# 8 -->  "KEYCODE_1"
# 9 -->  "KEYCODE_2"
# 10 -->  "KEYCODE_3"
# 11 -->  "KEYCODE_4"
# 12 -->  "KEYCODE_5"
# 13 -->  "KEYCODE_6"
# 14 -->  "KEYCODE_7"
# 15 -->  "KEYCODE_8"
# 16 -->  "KEYCODE_9"
# 17 -->  "KEYCODE_STAR"
# 18 -->  "KEYCODE_POUND"
# 19 -->  "KEYCODE_DPAD_UP"
# 20 -->  "KEYCODE_DPAD_DOWN"
# 21 -->  "KEYCODE_DPAD_LEFT"
# 22 -->  "KEYCODE_DPAD_RIGHT"
# 23 -->  "KEYCODE_DPAD_CENTER"
# 24 -->  "KEYCODE_VOLUME_UP"
# 25 -->  "KEYCODE_VOLUME_DOWN"
# 26 -->  "KEYCODE_POWER"
# 27 -->  "KEYCODE_CAMERA"
# 28 -->  "KEYCODE_CLEAR"
# 29 -->  "KEYCODE_A"
# 30 -->  "KEYCODE_B"
# 31 -->  "KEYCODE_C"
# 32 -->  "KEYCODE_D"
# 33 -->  "KEYCODE_E"
# 34 -->  "KEYCODE_F"
# 35 -->  "KEYCODE_G"
# 36 -->  "KEYCODE_H"
# 37 -->  "KEYCODE_I"
# 38 -->  "KEYCODE_J"
# 39 -->  "KEYCODE_K"
# 40 -->  "KEYCODE_L"
# 41 -->  "KEYCODE_M"
# 42 -->  "KEYCODE_N"
# 43 -->  "KEYCODE_O"
# 44 -->  "KEYCODE_P"
# 45 -->  "KEYCODE_Q"
# 46 -->  "KEYCODE_R"
# 47 -->  "KEYCODE_S"
# 48 -->  "KEYCODE_T"
# 49 -->  "KEYCODE_U"
# 50 -->  "KEYCODE_V"
# 51 -->  "KEYCODE_W"
# 52 -->  "KEYCODE_X"
# 53 -->  "KEYCODE_Y"
# 54 -->  "KEYCODE_Z"
# 55 -->  "KEYCODE_COMMA"
# 56 -->  "KEYCODE_PERIOD"
# 57 -->  "KEYCODE_ALT_LEFT"
# 58 -->  "KEYCODE_ALT_RIGHT"
# 59 -->  "KEYCODE_SHIFT_LEFT"
# 60 -->  "KEYCODE_SHIFT_RIGHT"
# 61 -->  "KEYCODE_TAB"
# 62 -->  "KEYCODE_SPACE"
# 63 -->  "KEYCODE_SYM"
# 64 -->  "KEYCODE_EXPLORER"
# 65 -->  "KEYCODE_ENVELOPE"
# 66 -->  "KEYCODE_ENTER"
# 67 -->  "KEYCODE_DEL"
# 68 -->  "KEYCODE_GRAVE"
# 69 -->  "KEYCODE_MINUS"
# 70 -->  "KEYCODE_EQUALS"
# 71 -->  "KEYCODE_LEFT_BRACKET"
# 72 -->  "KEYCODE_RIGHT_BRACKET"
# 73 -->  "KEYCODE_BACKSLASH"
# 74 -->  "KEYCODE_SEMICOLON"
# 75 -->  "KEYCODE_APOSTROPHE"
# 76 -->  "KEYCODE_SLASH"
# 77 -->  "KEYCODE_AT"
# 78 -->  "KEYCODE_NUM"
# 79 -->  "KEYCODE_HEADSETHOOK"
# 80 -->  "KEYCODE_FOCUS"
# 81 -->  "KEYCODE_PLUS"
# 82 -->  "KEYCODE_MENU"
# 83 -->  "KEYCODE_NOTIFICATION"
# 84 -->  "KEYCODE_SEARCH"
# 85 -->  "TAG_LAST_KEYCODE"
