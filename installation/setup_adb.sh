#!/bin/sh

sudo dpkg --configure -a
sudo apt-get install -y android-tools-adb android-tools-fastboot
