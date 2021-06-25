#!/usr/bin/env python3
import sys
sys.path.append('../../python')

from fetchUI import *

import unittest
import os
from testdata import *

class TestFetchUI(unittest.TestCase):
    #====== process_device ========
    def test_xml_parse(self):
        result = parseXML(testData)
        self.assertEqual(result.tag, "hierarchy")
        self.assertEqual(len(result.findall(f".//node")), 34)

    def test_xml_parse_options_data(self):
        result = parseXML(None, {"xml": testData})
        self.assertEqual(result.tag, "hierarchy")
        self.assertEqual(len(result.findall(f".//node")), 34)

    def test_xml_parse_options_file(self):
        path = os.path.join(os.getcwd(), "rawXml.xml")
        result = parseXML(None, {"file": path})
        self.assertEqual(result.tag, "hierarchy")
        self.assertEqual(len(result.findall(f".//node")), 34)

    def test_xml_find_node(self):
        root = parseXML(testData)
        searchStr = './/node[@text="Second label"]'
        result = root.findall(searchStr)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].tag, "node")
        self.assertEqual(result[0].attrib["class"], "android.widget.TextView")
    #=========================
if __name__ == "__main__":
    unittest.main()
