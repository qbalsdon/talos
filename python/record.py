#!/usr/bin/env python3
import sys
import os
import subprocess
import signal
import time
import tempfile
from datetime import datetime
from simplifier import setUp
from subprocess import Popen

record_usage="record [-s device]"

def time_stamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M")

def temp_file(name):
    return os.path.join(tempfile.gettempdir(), name)

def get_desktop():
    return os.path.expanduser("~/Desktop")

if __name__ == "__main__":
    options = setUp(ui_required = False)
    device = options.get("device")
    # print(createTimeStamp())
    recording_file = temp_file("recording.mp4")
    process_id_file = temp_file("process_id")

    print(recording_file)
    log_file = open(temp_file("log.txt"), "w")
    log_file.write("LOG FILE: " + time_stamp())

    if (os.path.exists(recording_file)):
        print("Recording stopped")
        with open(process_id_file, "r") as file:
            pid = file.read()
            print("READ PID: " + pid)
            os.kill(int(pid), signal.SIGTERM)
            file.close()
        os.rename(recording_file, os.path.join(get_desktop(), "{}.{}".format(time_stamp(),".mp4")))
    else:
        print("Recording started")
        process = Popen(['scrcpy', '-s', device, '-Nr', recording_file], stdout=log_file, stderr=log_file)
        with open(process_id_file, "w") as file:
            process_id = str(process.pid)
            print("WRITE PID:" + process_id)
            file.write(process_id)
            file.close()
    log_file.close()
    sys.exit(0)
