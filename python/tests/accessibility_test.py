#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

from accessibility import *

class TestAccessibility(unittest.TestCase):
    def test_validateArgs_none_returns_toggle(self):
        try:
            self.assertEqual(validateArgs(), None)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_empty_returns_toggle(self):
        try:
            result = validateArgs([])
            self.assertEqual(result, None)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_device_no_interference(self):
        try:
            #the device could have this name
            result = validateArgs(["-s","--portrait"])
            self.assertEqual(result, None)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_toggle_returns_toggle(self):
        try:
            result = validateArgs(["-s","deviceName", "--toggle"])
            self.assertEqual(result, None)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_t_returns_toggle(self):
        try:
            result = validateArgs(["-s","deviceName", "-t"])
            self.assertEqual(result, None)
        except Exception as e:
            self.fail("Should pass with no arguments")

    def test_validateArgs_short(self):
        test_subjects = {
            "-t":None,
            "-d":"com.android.talkback/com.google.android.marvin.talkback.TalkBackService",
            "-sr":"com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService:com.balsdon.accessibilityDeveloperService/.AccessibilityDeveloperService",
            "-ac":"com.google.android.apps.accessibility.auditor/com.google.android.apps.accessibility.auditor.ScannerService:com.android.talkback/com.google.android.marvin.talkback.TalkBackService"
        }
        for test_subject in test_subjects:
            self.assertEqual(validateArgs([test_subject]), test_subjects[test_subject])

    def test_validateArgs_short(self):
        test_subjects = {
            "--toggle":None,
            "--disable":"com.android.talkback/com.google.android.marvin.talkback.TalkBackService",
            "--screenreader":"com.google.android.marvin.talkback/com.google.android.marvin.talkback.TalkBackService:com.balsdon.accessibilityDeveloperService/.AccessibilityDeveloperService",
            "--accessibilityscanner":"com.google.android.apps.accessibility.auditor/com.google.android.apps.accessibility.auditor.ScannerService:com.android.talkback/com.google.android.marvin.talkback.TalkBackService"
        }
        for test_subject in test_subjects:
            self.assertEqual(validateArgs([test_subject]), test_subjects[test_subject])

    def test_validateArgs_fails_with_conflict(self):
        try:
            result = validateArgs(["-d", "-sr"])
            self.fail("Should fail with conflicting arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_fails_with_two_params(self):
        try:
            result = validateArgs(["--weird", "-weird2"])
            self.fail("Should fail with conflicting arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

    def test_validateArgs_fails_with_unknown(self):
        try:
            result = validateArgs(["--weird"])
            self.fail("Should fail with unknown arguments")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)

if __name__ == "__main__":
    unittest.main()
