#!/usr/bin/env python3
import unittest
import sys
sys.path.append('../../python')

from enums import orientation

class TestEnums(unittest.TestCase):
    def test_convertToAndroidValue_portrait_0(self):
        testSubject = orientation.PORTRAIT
        self.assertEqual(testSubject.convertToAndroidValue(0), 0)
        self.assertEqual(testSubject.convertToAndroidValue(1), 0)

    def test_convertToAndroidValue_landscape_1(self):
        testSubject = orientation.LANDSCAPE
        self.assertEqual(testSubject.convertToAndroidValue(0), 1)
        self.assertEqual(testSubject.convertToAndroidValue(1), 1)

    def test_convertToAndroidValue_toggle_inverts(self):
        testSubject = orientation.TOGGLE
        self.assertEqual(testSubject.convertToAndroidValue(0), 1)
        self.assertEqual(testSubject.convertToAndroidValue(1), 0)

    def test_convertToAndroidValue_toggle_throws(self):
        testValues = [-2, -1, 2, 3, 4, 5]
        testSubjects = [orientation.PORTRAIT, orientation.LANDSCAPE,orientation.TOGGLE]
        for test_subject in testSubjects:
            for test_value in testValues:
                try:
                    test_subject.convertToAndroidValue(test_value)
                    self.fail(str(test_value) + " is not a valid number")
                except Exception as e:
                    self.assertTrue(e.__class__ is ValueError)

if __name__ == "__main__":
    unittest.main()
