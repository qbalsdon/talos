#!/usr/bin/env python3
import sys
sys.path.append('../../python')

from midOf import *
from fetchUI import *

import unittest
from testdata import *

class TestMidOf(unittest.TestCase):

    DEVICE_NAME = "deviceName"

    def test_validateArgs_none(self):
        self.assertFalse(validateArgs(None))

    def test_validateArgs_empty(self):
        self.assertFalse(validateArgs({}))

    def test_validateArgs_element(self):
        self.assertTrue(validateArgs({"element": "elementName"}))

    def test_validateArgs_property_no_value(self):
        self.assertFalse(validateArgs({"property": "propertyValue"}))

    def test_validateArgs_property_and_value(self):
        self.assertTrue(validateArgs({"property": "propertyValue", "value": "valueText"}))

    def test_midOf_element(self):
        result = midOf({"element": "RUN CURRENT DEBUG ACTION"}, parseXML(data = testData))
        self.assertEqual(result, {"x": 1024,"y": 132})

    def test_midOf_element_partial(self):
        result = midOf({"element": "rent deb"}, parseXML(data = testData))
        self.assertEqual(result, {"x": 1024,"y": 132})

    #resource-id="com.balsdon.accessibilityDeveloperService:id/volumeLabel"
    def test_midOf_property_partial(self):
        result = midOf({"property": "resource-id", "value": "volumeLabel"}, parseXML(data = testData))
        self.assertEqual(result, {'x': 146, 'y': 102})

if __name__ == "__main__":
    unittest.main()
