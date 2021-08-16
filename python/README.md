# Python conversion

An attempt at Python TDD.

## TODO (Commands):

1. alternate dark mode
1. alternate brightness
    adb shell settings put system screen_brightness 0
1. alternate animations
1. alternate show taps
1. alternate show layout (`adb shell setprop debug.layout true && adb shell service call activity 1599295570` https://susuthapa19961227.medium.com/enable-layout-debugging-in-android-using-adb-64016d755441)
1. alternate colour inversion
1. alternate density toggle
    SECURE
        display_density_forced [None, 374.0, 540.0, '']
1. Clean up naming conventions
1. have a unary arguments processor in common.
   - just single arguments
   - multiple arguments (optionals, required, one of, multiples)

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

## TODO: UI

1. create UI with buttons
1. draw wireframe UI
