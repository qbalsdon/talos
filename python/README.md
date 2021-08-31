# Python conversion

An attempt at Python TDD.

## TODO (Commands):

1. print device state (animations on, rtl, darkmode, etc.)
1. Clean up naming conventions
1. have a unary arguments processor in common.
   - just single arguments
   - multiple arguments (optionals, required, one of, multiples)
1. List all
  - accessibility headings
  - links
  - image content descriptions


1. :white_check_mark: get the current device, read from parameters
1. :white_check_mark: get the UI as XML and format
1. :white_check_mark: get the mid of a component
1. :white_check_mark: tap an element
1. :white_check_mark: create the alternator structure
1. :white_check_mark: alternate orientations
1. :white_check_mark: alternate talkback services
   1. :x: add switch access?  
1. :white_check_mark: alternate font scale
1. :white_check_mark: alternate RTL
1. :white_check_mark: open different menus: accessibility, developer settings
1. :white_check_mark: Get the current activity on screen
1. :white_check_mark: activities: list current activity on screen (adb shell dumpsys window | grep mCurrentFocus)
1. :white_check_mark: listElements
1. :white_check_mark: keycodes
1. :white_check_mark: swipe based on screen size
1. :white_check_mark: unlockWithSwipe
1. :white_check_mark: recordOn / recordOff
1. :white_check_mark: ~checkOnScreen~ hasElements
1. :white_check_mark: bash script to execute all tests
1. :white_check_mark: alternate dark mode
1. :white_check_mark: alternate brightness
1. :white_check_mark: alternate animations
1. :white_check_mark: alternate show taps
1. :white_check_mark: alternate show layout (`adb shell setprop debug.layout true && adb shell service call activity 1599295570`)
1. :white_check_mark: alternate density toggle
1. :white_check_mark: check why the following are not working:
   - :white_check_mark: forcertl <-- somehow now needs a rattle and opening locale settings
   - :white_check_mark: density <-- `adb shell wm density`
   - :white_check_mark: animation

## TODO: UI

1. create UI with buttons
1. draw wireframe UI

## Special thanks

- Suson Thapa, ["Enable layout debugging in Android using ADB"][0]
- gamingexpert13 [answer on "adb command to open settings and change them"][1]
- ["How to Change DPI Density on Android Without Root"][2]

[0]: https://susuthapa19961227.medium.com/enable-layout-debugging-in-android-using-adb-64016d755441
[1]: https://stackoverflow.com/a/68655882/932052
[2]: https://www.droidviews.com/change-dpi-density-on-android-without-root/
