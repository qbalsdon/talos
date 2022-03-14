#!/usr/bin/env python3

import tkinter as tk
import time
import threading
import random
import queue

from tkinter import ttk
from tkinter import Menu
from tkinter import simpledialog
from tkinter import filedialog as fd

from menu_builder import *

from action_map import *

from xml_viewer import XML_Viewer

class GuiPart:

    def clear_frame(self, container):
        for widget in container.winfo_children():
           widget.destroy()
        container.pack_forget()

    def device_name_formatted(self, device_serial):
        name = get_device_name(device_serial)
        if name == None:
            name = device_serial
        else:
            name = f"{name} ({device_serial[0:5]}...)"
        return name

    def populate_devices_frame(self, container):
        self.clear_frame(container)
        previous_selection = []
        for var in self.user_devices:
            if len(var.get()) > 0:
                previous_selection.append(var.get())

        self.user_devices = []
        devices_list = get_device_list()
        if devices_list.splitlines()[0] != 'List of devices attached':
            current_row = 0
            for line in devices_list.splitlines():
                data = line.split("\t")
                selected_device = tk.StringVar()
                name = self.device_name_formatted(data[0])
                device_check = ttk.Checkbutton(
                    container,
                    text=name,
                    onvalue=data[0],
                    offvalue="",
                    variable=selected_device)
                if data[0] in previous_selection:
                    selected_device.set(data[0])
                self.user_devices.append(selected_device)
                device_check.pack(fill=tk.X, side=tk.TOP)
                current_row = current_row + 1

    def create_device_frame(self, container):
        devices_frame = ttk.Frame(container)
        devices_frame.grid(row=1, column=0, columnspan=1, sticky='NW')
        self.populate_devices_frame(devices_frame)
        return devices_frame

    def selected_device_list(self):
        mapped = list(map((lambda var: var.get()), self.user_devices))
        return list(filter(lambda value: len(value) > 0, mapped))

    def find_file(self):
        filename = fd.askopenfilename()
        return filename

    def get_user_input(self, prompt):
        return simpledialog.askstring(title="Input", prompt=prompt)

    def create_window_table(self, root, title, data, show_names=False):
        window = tk.Toplevel(root)
        window.title(title)
        row = 0
        for key in data.keys():
            label = ttk.Label(window, text=key, borderwidth=2, relief="solid")
            label.grid(row=row, column=0, sticky='WE')
            next_col = 1
            if show_names:
                name = get_device_name(key)
                if name == key:
                    name = "..."
                label = ttk.Label(window, text=name, borderwidth=2, relief="solid")
                label.grid(row=row, column=next_col, sticky='WE')
                next_col = next_col + 1
            text = ttk.Label(window, text=data[key], borderwidth=2, relief="solid")
            text.grid(row=row, column=next_col, sticky='WE')
            row = row + 1

    def show_table(self, root, device_data):
        if isinstance(list(device_data.items())[0][1], str):
            self.create_window_table(root, "Summary", device_data, True)
        else:
            for data in device_data:
                self.create_window_table(root, self.device_name_formatted(data), device_data[data])

    def create_xml_window(self, root, title, xml):
        window = tk.Toplevel(root)
        window.title(title)
        XML_Viewer(window, xml, heading_text=title).pack(fill='both', expand=True)

    def show_xml(self, root, device_data):
        for device in device_data:
            self.create_xml_window(root, self.device_name_formatted(device), device_data[device])

    def key(self, event):
        if event.char == event.keysym:
            msg = 'Normal Key %r' % event.char
        elif len(event.char) == 1:
            msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
        else:
            msg = 'Special Key %r' % event.keysym
        print(f"key event: {msg}")

    def __init__(self, root, queue, endCommand):
        self.queue = queue
        self.user_devices = []
        # Set up the GUI
        root.title('ADB Controller')
        icon = tk.PhotoImage(file = 'android.png')
        root.iconphoto(False, icon)

        action_mapper = ActionMapper(
            self.selected_device_list,
            self.find_file,
            self.get_user_input,
            lambda data: self.show_table(root, data),
            lambda data: self.show_xml(root, data),
            lambda: root.destroy())
        create_menu(root, action_mapper.action_map)
        self.devices_frame = self.create_device_frame(root)
        self.devices_frame.grid(row=0, column=0, sticky='NW')
        root.bind_all('<Key>', self.key)
        # Add more GUI stuff here depending on your specific needs

    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                self.populate_devices_frame(self.devices_frame)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
            except Queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.
            time.sleep(rand.random() * 1.5)
            msg = rand.random()
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0

rand = random.Random()
root = tk.Tk()

client = ThreadedClient(root)
root.mainloop()
