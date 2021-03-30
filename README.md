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

## SCRCPY
https://github.com/Genymobile/scrcpy/blob/master/BUILD.md \
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
