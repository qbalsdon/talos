#!/usr/bin/env python3
import sys
sys.path.append('../../python')

from hasElement import *
from testdata import *
from simplifier import parseXML

import unittest

class TestSimplifier(unittest.TestCase):

    def test_validateArgs_one(self):
        test_args = ["-s", "DEVICE", "key:value"]
        test_subject = validateArgs(test_args)
        self.assertEqual(test_subject, {"key":"value"})
        test_args = ["key:value"]
        test_subject = validateArgs(test_args)
        self.assertEqual(test_subject, {"key":"value"})

    def test_validateArgs_id_to_resource_id(self):
        test_args = ["-s", "DEVICE", "id:value"]
        test_subject = validateArgs(test_args)
        self.assertEqual(test_subject, {"resource-id":"value"})
        test_args = ["id:value"]
        test_subject = validateArgs(test_args)
        self.assertEqual(test_subject, {"resource-id":"value"})
        test_args = ["key:pair", "id:value"]
        test_subject = validateArgs(test_args)
        self.assertEqual(test_subject, {"key":"pair", "resource-id":"value"})

    def test_validateArgs_two(self):
        expected = {"key":"value", "key1":"value1"}
        test_args = ["-s", "DEVICE", "key:value", "key1:value1"]

        test_subject = validateArgs(test_args)
        self.assertEqual(test_subject, expected)
        test_args = ["key:value", "key1:value1"]
        test_subject = validateArgs(test_args)
        self.assertEqual(test_subject, expected)

    def test_validateArgs_nothing(self):
        test_args = ["-s", "DEVICE"]
        try:
            test_subject = validateArgs(test_args)
            self.fail("No parameters should raise ValueError")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)
        try:
            test_subject = validateArgs(None)
            self.fail("No parameters should raise ValueError")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)
        try:
            test_subject = validateArgs([])
            self.fail("No parameters should raise ValueError")
        except Exception as e:
            self.assertTrue(e.__class__ is ValueError)


    def test_findMatchingElements_one(self):
        root = parseXML(testData)
        lookFor = {"resource-id": "volumeDown"}
        test_subject = findMatchingElements(root, lookFor)
        self.assertEqual(len(test_subject), 1)

    def test_findMatchingElements_more_attributes(self):
        root = parseXML(testData)
        lookFor = {"text":"RUN CURRENT DEBUG ACTION", "resource-id":"debugAction"}
        test_subject = findMatchingElements(root, lookFor)
        self.assertEqual(len(test_subject), 1)

    def test_findMatchingElements_more_attributes_fails(self):
        root = parseXML(testData)
        lookFor = {"text":"RUN CURRENT DEBUG ACTION", "resource-id":"debugAction1"}
        test_subject = findMatchingElements(root, lookFor)
        self.assertEqual(len(test_subject), 0)

    def test_findMatchingElements_more_elements(self):
        root = parseXML(testData)
        lookFor = {"class":"android.widget.ImageButton"}
        test_subject = findMatchingElements(root, lookFor)
        self.assertEqual(len(test_subject), 2)

if __name__ == "__main__":
    unittest.main()
