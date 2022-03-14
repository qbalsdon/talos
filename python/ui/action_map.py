#!/usr/bin/env python3

from interactor import *
import os
import json

class ActionMapper:

    def execute_command(self, command):
        run_on_all_selected_devices(command, self.selected_devices_lambda())

    def get_wifi_credentials(self):
        return get_system_data('WIFI_INFO')

    def get_login_details(self):
        return get_system_data('USER_INFO')["login"]

    def create_wifi_option(self):
        list = self.get_wifi_credentials()
        map = {}
        for wifi_name in list:
            password = list[wifi_name]["password"]
            map[wifi_name] = lambda pwd=password: device_type(self.selected_devices_lambda(), pwd)
        return map

    def create_login_option(self):
        list = self.get_login_details()
        map = {}
        for login_option in list:
            user = login_option["username"]
            password = login_option["password"]
            map[user] = lambda usr=user, pwd=password: device_enter_login_details(self.selected_devices_lambda(), usr, pwd)
        return map

    def create_screen_options(self):
        list = screen_options
        map = {}
        for element in list:
            name = element.replace("_", " ").title()
            map[name] = lambda opt=element: device_open_activity(self.selected_devices_lambda(), opt)
        return map

    def get_user_input(self, prompt):
        text = self.user_input(prompt)
        device_type(self.selected_devices_lambda(), text)

    def run_update(self):
        file_name = self.file_select()
        device_update(self.selected_devices_lambda(), file_name)

    def get_input_then(self, prompt, fn):
        text = self.user_input(prompt)
        fn(text)

    def get_device_report(self):
        devices = self.selected_devices_lambda()
        package = get_focus_app()

        package_specific_data = {
            "versionCode": "Version Code",
            "versionName": "Version Name",
        }

        device_specific_data = {
            "ro.build.display.id" : "App Firmware Version"
        }

        package_info = {}
        for key in package_specific_data:
            raw_data = device_get_info(devices, package, key)
            package_info[key] = device_get_info(devices, package, key)

        device_info = {}
        for key in device_specific_data:
            device_info[key] = device_get_system_property_info(devices, key)

        report = {}
        for device in devices:
            report[device] = {}
            for package_key in package_info:
                # print(f"  package_info[{package_key}][{device}]")
                raw_data = package_info[package_key][device]
                data = raw_data
                if package_key in raw_data:
                    for element in raw_data.split(" "):
                        if package_key in element:
                            data = element.replace(f"{package_key}=", "")
                            break;
                report[device][package_key] = data
            for device_key in device_info:
                report[device][device_key] = device_info[device_key][device]
        self.show_table(report)

    def get_current_activity(self):
        devices = self.selected_devices_lambda()
        report = get_current_activity_name(devices)
        self.show_table(report)

    def get_ui_report(self):
        devices = self.selected_devices_lambda()
        report = device_get_ui(devices)
        self.show_xml(report)

    def set_language(language, code):
        # device_set_language(self.selected_devices_lambda(), language, code)
        print("TODO: set language")

    def __init__(self, selected_devices_lambda, file_select_lambda, user_input_lambda, show_table_lambda, show_xml_lambda, exit_lambda):
        self.selected_devices_lambda = selected_devices_lambda
        self.file_select = file_select_lambda
        self.user_input = user_input_lambda
        self.show_table = show_table_lambda
        self.show_xml = show_xml_lambda
        self.exit = exit_lambda
        self.action_map = {
            "File": {
                "About" : lambda: print("TODO: Show about screen"),
                "scrcpy": lambda: self.execute_command(device_scrcpy),
                "record": lambda: self.execute_command(device_record),
                "kill scrcpy": lambda: run_command(["pkill","scrcpy"]),
                "Exit" : lambda: self.exit(),
            },
            "Input": {
                "Custom" : lambda: self.get_user_input("What do you want to type?"),
                "Buttons": {
                    "Power" : lambda: self.execute_command(device_power),
                    "Back" : lambda: self.execute_command(device_back),
                    "Home" : lambda: self.execute_command(device_home),
                    "Reboot" : lambda: self.execute_command(device_reboot),
                },
                "Logins" : self.create_login_option(),
                "Wifi" : self.create_wifi_option(),
            },
            "Android": {
                "Current activity": lambda: self.get_current_activity(),
                "Open Android Settings": lambda: device_open_screen(self.selected_devices_lambda(), "android.settings.SETTINGS"),
                "System Report": lambda: self.get_device_report(),
                "UI Report": lambda: self.get_ui_report(),
                "Quick Navigate": self.create_screen_options(),
                "Display":{
                    "Contrast (Max)": lambda: device_screen_brightness(self.selected_devices_lambda(), 100),
                    "Contrast (Min)": lambda: device_screen_brightness(self.selected_devices_lambda(), 1),
                    "Dim 5  Min": lambda: device_screen_timeout(self.selected_devices_lambda(), 300000),
                    "Dim 15 Sec": lambda: device_screen_timeout(self.selected_devices_lambda(), 15000),
                    "Dim 5  Sec": lambda: device_screen_timeout(self.selected_devices_lambda(), 5000)
                },
                # "Language": {
                #     "Show Language Screen": lambda: device_open_activity(self.selected_devices_lambda(), "locale"),
                #     "English (GB)" : lambda: self.set_language("en", "GB"),
                #     "English (US)" : lambda: self.set_language("en", "US"),
                #     "German" : lambda: self.set_language("de", "DE"),
                #     "Hebrew" : lambda: self.set_language("iw", "IL"),
                #     "Urdu" : lambda: self.set_language("ur", "IN"),
                # },
            },
            "Misc": {
                "Sound down": lambda: device_sound_down(self.selected_devices_lambda()),
                "App Settings": lambda: device_open_app_settings(self.selected_devices_lambda()),
                "Update": lambda: self.run_update(),
                "Properties" :{
                    "Clear" : lambda: device_clear_qa_settings(self.selected_devices_lambda()),
                    "No update": lambda: device_app_no_update(self.selected_devices_lambda()),
                },
                "Clear cache": lambda: device_clear_cache(self.selected_devices_lambda(), get_focus_app())
            },
            "A11y": {
                "TalkBack" : {
                    "Turn off": lambda: device_turn_on_accessibility_service(self.selected_devices_lambda(), "disable"),
                    "Developer tools (with Screen Reader)": lambda: device_turn_on_accessibility_service(self.selected_devices_lambda(), "screenreader"),
                    "Scanner": lambda: device_turn_on_accessibility_service(self.selected_devices_lambda(), "accessibilityscanner"),
                },
                "Dark mode": lambda: device_dark_mode_toggle(self.selected_devices_lambda()),
                "Font size": {
                    "Toggle": lambda: device_font_scale(self.selected_devices_lambda(), None),
                    "Small": lambda: device_font_scale(self.selected_devices_lambda(), 0.85),
                    "Default": lambda: device_font_scale(self.selected_devices_lambda(), 1),
                    "Large": lambda: device_font_scale(self.selected_devices_lambda(), 1.15),
                    "Largest": lambda: device_font_scale(self.selected_devices_lambda(), 1.3),
                    "Custom": lambda: self.get_input_then("Please enter font scale",lambda input: device_font_scale(self.selected_devices_lambda(), input)),
                },
                "Developer tools": {
                    "Right": lambda: device_accessibility_action(self.selected_devices_lambda(), "ACTION_SWIPE_RIGHT"),
                    "Left": lambda: device_accessibility_action(self.selected_devices_lambda(), "ACTION_SWIPE_LEFT"),
                    "Up": lambda: device_accessibility_action(self.selected_devices_lambda(), "ACTION_SWIPE_UP"),
                    "Down": lambda: device_accessibility_action(self.selected_devices_lambda(), "ACTION_SWIPE_DOWN"),
                    "Volume": {
                        "Up": lambda: device_accessibility_action(self.selected_devices_lambda(), "ACTION_VOLUME_UP"),
                        "Down": lambda: device_accessibility_action(self.selected_devices_lambda(), "ACTION_VOLUME_DOWN"),
                        "Mute": lambda: device_accessibility_action(self.selected_devices_lambda(), "ACTION_VOLUME_MUTE"),
                    },
                    "A11y Menu": lambda: device_accessibility_action(self.selected_devices_lambda(), "ACTION_SWIPE_UP_RIGHT"),
                    "A11y Curtain": lambda: device_accessibility_action(self.selected_devices_lambda(), "ACTION_CURTAIN"),
                    "Say": lambda: print("Show an input dialog to say something")
                },
                "Toogle RTL" : lambda: device_force_rtl(self.selected_devices_lambda()),
                "A11y Settings": lambda: device_open_activity(self.selected_devices_lambda(), "accessibility"),
            },
        }
