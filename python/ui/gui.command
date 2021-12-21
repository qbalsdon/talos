#!/usr/bin/env python3
import os

import tkinter as tk
from tkinter import ttk

import subprocess
import sys

from interactor import *

def clear_frame(container):
    for widget in container.winfo_children():
       widget.destroy()
    container.pack_forget()

def not_blank(value):
    return len(value) > 0

def device_list():
    global user_devices
    mapped = list(map((lambda var: var.get()), user_devices))
    return list(filter(not_blank, mapped))


def validate_then(fn):
    list = device_list()
    if (len(list) > 0):
        fn(list)

def wifi_password_clicked():
    try:
        password = os.environ['WIFI_PASSWORD']
        validate_then(lambda devices: device_type(devices, password))
    except KeyError as err:
        print("No password set")
        # tkinter.simpledialog.askstring("Password", "Type Wifi Password",password)

def populate_devices_frame(container):
    global user_devices
    clear_frame(container)
    user_devices = []
    devices_list=subprocess.run(["adb","devices"], capture_output=True).stdout.decode().strip().split('\n', 1)[-1]
    current_row = 0
    for line in devices_list.splitlines():
        data = line.split("\t")
        selected_device = tk.StringVar()
        device_check = ttk.Checkbutton(
            container,
            text=data[0] + " [" + data[1] + "]" ,
            onvalue=data[0],
            offvalue="",
            variable=selected_device)
        user_devices.append(selected_device)
        device_check.pack(fill=tk.X, side=tk.TOP)
        current_row = current_row + 1

def create_button_frame(container):
    frame = ttk.Frame(container)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=3)
    frame.columnconfigure(1, weight=3)

    buttons = {
        "Unlock": lambda: validate_then(device_unlock),
        "Power": lambda: validate_then(device_power),
        "Back": lambda: validate_then(device_back),
        "scrcpy": lambda: validate_then(device_scrcpy),
        "Home": lambda: validate_then(device_home),
        "Wifi Password":wifi_password_clicked
    }
    row = 0
    for text, event in buttons.items():
        ttk.Button(frame, text=text, command=event).grid(column=0, row=row, sticky='NW')
        row = row + 1

    return frame

def create_left_frame(container):
    frame = ttk.Frame(container)
    ttk.Button(frame, text='Refresh', command=lambda:populate_devices_frame(devices_frame)).grid(row=0, column=0, columnspan=1, sticky='NW')
    devices_frame = ttk.Frame(frame)
    devices_frame.grid(row=1, column=0, columnspan=1, sticky='NW')
    populate_devices_frame(devices_frame)

    return frame

def create_main_window():
    # root window
    root = tk.Tk()
    root.title('ADB Controller')
    icon = tk.PhotoImage(file = 'android.png')
    root.iconphoto(False, icon)
    # root.geometry('500x500')
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)

    left_frame = create_left_frame(root)
    left_frame.grid(row=0, column=0, sticky='NW')

    button_frame = create_button_frame(root)
    button_frame.grid(row=0, column=1)

    root.mainloop()

def __init__(self):
    self.user_devices = []

if __name__ == "__main__":
    create_main_window()
