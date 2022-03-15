#!/usr/bin/env python3

import tkinter as tk
from tkinter import Menu

def create_dropdown(parent, list_name, action_list, key_binding):
    menu_item = Menu(
        parent,
        tearoff=0
    )
    for key in action_list:
        if type(action_list[key]) is dict:
            menu_item.add_separator()
            menu_item.add_cascade(
                label=key,
                menu=create_dropdown(menu_item, key, action_list[key], key_binding)
            )
        elif type(action_list[key]) is list:
            menu_item.add_command(
                label=key,
                command=action_list[key][0],
                accelerator=action_list[key][1]
            )
            key_binding[action_list[key][1]] = action_list[key][0]
        else:
            menu_item.add_command(
                label=key,
                command=action_list[key]
            )
    return menu_item

def create_menu(root_window, action_map):
    menubar = Menu(root_window)
    key_binding = {}
    root_window.config(menu=menubar)

    for header_item in action_map:
        # print(f"Found: {header_item}")
        menubar.add_cascade(
            label=header_item,
            menu=create_dropdown(menubar, header_item, action_map[header_item], key_binding),
            underline=0
        )
    return menubar, key_binding
