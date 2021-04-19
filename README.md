# talos

This is a Raspberry Pi project, but should work on any linux system with adb.

## Installation for Raspberry Pi

From the command line, run
```
wget -O - https://raw.githubusercontent.com/qbalsdon/talos/main/installation/setup_adb.sh | sudo sh
wget -O - https://raw.githubusercontent.com/qbalsdon/talos/main/installation/setup_scrcpy.sh | sudo sh
```

# Helpful
Reset VNC `sudo Xvnc -generatekeys force`

# References
## ADB
https://gist.github.com/kibotu/849ea0f113f0093ea14a90f373f7eb1e
https://raspberrypi.stackexchange.com/questions/44005/how-do-i-install-the-android-debug-bridge-adb-on-a-raspberry-pi

### [Useful ADB commands][0]

1. `adb shell settings list [secure|global|system]`

This is the manner in which developers can see what is available for modification on the system normally it may be retrieved by calling: `adb shell settings get [secure|global|system] [name]` and set by calling `adb shell settings put [secure|global|system] [name] [value]`

I have made this a little simpler with my `sysDiff` script.

Really useful [cheatsheet][1]

#### ADB Basics

> adb devices (lists connected devices)
> adb root (restarts adbd with root permissions)
> adb start-server (starts the adb server)
> adb kill-server (kills the adb server)
> adb reboot (reboots the device)
> adb devices -l (list of devices by product/model)
> adb shell (starts the backround terminal)
> exit (exits the background terminal)
> adb help (list all commands)
> adb -s <deviceName> <command> (redirect command to specific device)
> adb –d <command> (directs command to only attached USB device)
> adb –e <command> (directs command to only attached emulator)

#### Package Installation

> adb shell install <apk> (install app)
> adb shell install <path> (install app from phone path)
> adb shell install -r <path> (install app from phone path)
> adb shell uninstall <name> (remove the app)

#### Paths

> /data/data/<package>/databases (app databases)
> /data/data/<package>/shared_prefs/ (shared preferences)
> /data/app (apk installed by user)
> /system/app (pre-installed APK files)
> /mmt/asec (encrypted apps) (App2SD)
> /mmt/emmc (internal SD Card)
> /mmt/adcard (external/Internal SD Card)
> /mmt/adcard/external_sd (external SD Card)

> adb shell ls (list directory contents)
> adb shell ls -s (print size of each file)
> adb shell ls -R (list subdirectories recursively)

#### File Operations

> adb push <local> <remote> (copy file/dir to device)
> adb pull <remote> <local> (copy file/dir from device)
> run-as <package> cat <file> (access the private package files)

#### Phone Info

> adb get-statе (print device state)
> adb get-serialno (get the serial number)
> adb shell dumpsys iphonesybinfo (get the IMEI)
> adb shell netstat (list TCP connectivity)
> adb shell pwd (print current working directory)
> adb shell dumpsys battery (battery status)
> adb shell pm list features (list phone features)
> adb shell service list (list all services)
> adb shell dumpsys activity <package>/<activity> (activity info)
> adb shell ps (print process status)
> adb shell wm size (displays the current screen resolution)
> dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp' (print current app's opened activity)

#### Package Info

> adb shell list packages (list package names)
> adb shell list packages -r (list package name + path to apks)
> adb shell list packages -3 (list third party package names)
> adb shell list packages -s (list only system packages)
> adb shell list packages -u (list package names + uninstalled)
> adb shell dumpsys package packages (list info on all apps)
> adb shell dump <name> (list info on one package)
> adb shell path <package> (path to the apk file)

####  Configure Settings Commands

> adb shell dumpsys battery set level <n> (change the level from 0 to 100)
> adb shell dumpsys battery set status<n> (change the level to unknown, charging, discharging, not charging or full)
> adb shell dumpsys battery reset (reset the battery)
> adb shell dumpsys battery set usb <n> (change the status of USB connection. ON or OFF)
> adb shell wm size WxH (sets the resolution to WxH)

####  Device Related Commands

> adb reboot-recovery (reboot device into recovery mode)
> adb reboot fastboot (reboot device into recovery mode)
> adb shell screencap -p "/path/to/screenshot.png" (capture screenshot)
> adb shell screenrecord "/path/to/record.mp4" (record device screen)
> adb backup -apk -all -f backup.ab (backup settings and apps)
> adb backup -apk -shared -all -f backup.ab (backup settings, apps and shared storage)
> adb backup -apk -nosystem -all -f backup.ab (backup only non-system apps)
> adb restore backup.ab (restore a previous backup)
> adb shell am start|startservice|broadcast <INTENT>[<COMPONENT>]
>     -a <ACTION> e.g. android.intent.action.VIEW
>     -c <CATEGORY> e.g. android.intent.category.LAUNCHER (start activity intent)

> adb shell am start -a android.intent.action.VIEW -d URL (open URL)
> adb shell am start -t image/* -a android.intent.action.VIEW (opens gallery)

####  Logs

> adb logcat [options] [filter] [filter] (view device log)
> adb bugreport (print bug reports)

####  Permissions

> adb shell permissions groups (list permission groups definitions)
> adb shell list permissions -g -r (list permissions details)

## SCRCPY

https://github.com/Genymobile/scrcpy/blob/master/BUILD.md
DO NOT BUILD THE SERVER, THAT REQUIRES THE SDK

## Keyboard shortcuts

1. Copy the contents of the /mac folder to your local `/Users/[USERNAME]/Library/Services` folder.
1. Open `System Preferences -> Keyboard -> Shortcuts -> General`
1. Under `Services` assign some shortcuts!

### Uninstallation
```
sudo rm -rf /usr/local/bin/scrcpy
sudo rm -rf /usr/local/share/scrcpy/scrcpy-server
```

[0]: https://adbinstaller.com/commands/adb-shell-settings-5b670d5ee7958178a2955536
[1]: https://www.automatetheplanet.com/adb-cheat-sheet/
