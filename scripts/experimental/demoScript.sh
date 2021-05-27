#!/bin/sh
clear

function break_between {
  sleep 3
  clear
}

TIME=3
SPACER="\n----------------------------------------\n"

echo "I think it's only fair to inform the viewer that I scripted my scripts for this. That's just how much I love scripts"

break_between

echo "... also #automation"

break_between

echo "\n\n  ~~ Happy Global Accessibility Awareness Day 2021!! ~~"

break_between

echo "USE STANDARD ADB TO PRESS THE HOME BUTTON\n\n   > adb shell input keyevent KEYCODE_HOME"
adb shell input keyevent KEYCODE_HOME

break_between

echo "DISABLE TALKBACK FOR DEMO PURPOSES\n\n   > sh talkback -d"
sh talkback -d

break_between

echo "OPEN THE DEMO APP\n\n   > adb shell am start -n com.balsdon.accessibilityDeveloperService/com.balsdon.accessibilityDeveloperService.DemoActivity"
adb shell am start -n com.balsdon.accessibilityDeveloperService/com.balsdon.accessibilityDeveloperService.DemoActivity > /dev/null

break_between

echo "USE MY SCRIPT TO TOGGLE TALKBACK STATE\n\n   > sh talkback"
sh talkback

break_between

echo "CUSTOM COMMAND TO SWIPE RIGHT ON BEHALF OF THE USER\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_SWIPE_RIGHT\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_SWIPE_RIGHT" > /dev/null

break_between

echo "FIND AND FOCUS LINK BY TEXT\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_FOCUS_ELEMENT\" -e PARAMETER_TEXT \"Google.com\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_FOCUS_ELEMENT" -e PARAMETER_TEXT "Google.com" > /dev/null

break_between

echo "CUSTOM COMMAND TO SWIPE LEFT ON BEHALF OF THE USER\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_SWIPE_LEFT\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_SWIPE_LEFT" > /dev/null

break_between

echo "CUSTOM COMMAND TO NAVIGATE TO THE NEXT HEADING\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_FOCUS_ELEMENT\" -e PARAMETER_HEADING \"DIRECTION_FORWARD\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_FOCUS_ELEMENT" -e PARAMETER_HEADING "DIRECTION_FORWARD" > /dev/null

break_between

echo "REPEAT COMMAND (NAVIGATE TO THE NEXT HEADING)\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_FOCUS_ELEMENT\" -e PARAMETER_HEADING \"DIRECTION_FORWARD\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_FOCUS_ELEMENT" -e PARAMETER_HEADING "DIRECTION_FORWARD" > /dev/null

break_between

echo "FIND AND FOCUS BUTTON BY IDENTIFIER\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_FOCUS_ELEMENT\" -e PARAMETER_ID \"settingsButton\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_FOCUS_ELEMENT" -e PARAMETER_ID "settingsButton" > /dev/null

break_between

echo "CLICK THE BUTTON AS AN ACCESSIBILITY USER\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_CLICK\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_CLICK" > /dev/null

break_between

echo "PRESS THE BACK BUTTON\n\n   > adb shell input keyevent KEYCODE_BACK"
adb shell input keyevent KEYCODE_BACK > /dev/null

break_between

echo "~~ DEV CURTAIN TIME ~~"

break_between

echo "ENABLE THE CUSTOM DEVELOPER CURTAIN FOR ANDROID\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_CURTAIN\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_CURTAIN" > /dev/null

break_between

echo "PERFORM A RIGHT SWIPE\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_SWIPE_RIGHT\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_SWIPE_RIGHT" > /dev/null

break_between

echo "PERFORM ANOTHER RIGHT SWIPE\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_SWIPE_RIGHT\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_SWIPE_RIGHT" > /dev/null

break_between

echo "AND ONE MORE RIGHT SWIPE\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_SWIPE_RIGHT\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_SWIPE_RIGHT" > /dev/null

break_between

echo "FIND AND FOCUS HEADING BY TEXT\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_FOCUS_ELEMENT\" -e PARAMETER_TEXT \"Heading\ 3\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_FOCUS_ELEMENT" -e PARAMETER_TEXT "Heading\ 3" > /dev/null

break_between

echo "TURN OFF THE CURTAIN\n\n   > adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION \"ACTION_CURTAIN\""
adb shell am broadcast -a com.balsdon.talkback.accessibility -e ACTION "ACTION_CURTAIN" > /dev/null

break_between

echo "ENSURE TALKBACK IS OFF\n\n   > sh talkback -d"
sh talkback -d  > /dev/null

break_between

clear
cat GAAD.txt
sleep 10
