#!/usr/bin/env python3
import sys
sys.path.append('../../python')

from fetchUI import parseXML

import unittest
from testdata import testData
from listElements import parseXmlToList, filterList, pretty_print, max_col_lengths, pretty_print_line, clean_node, validateArgs

class TestListElements(unittest.TestCase):
    def test_xml_parse_to_list(self):
        result = parseXML(testData)
        self.assertEqual(result.tag, "hierarchy")
        self.assertEqual(len(result.findall(f".//node")), 34)

        nodeList = parseXmlToList(result)
        self.assertEqual(len(nodeList), 34)

    def test_filter_cols(self):
        cols = ["resource-id", "text", "class", "bounds"]
        rootNode = parseXML(testData)
        nodeList = parseXmlToList(rootNode)
        filtered = filterList(nodeList, cols)
        for element in filtered:
            self.assertEqual(len(element), 5)
            self.assertTrue("midOf" in element)
            for colName in cols:
                self.assertTrue(colName in element)

    def test_filter_cols(self):
        cols = ['text', 'resource-id', 'class', 'package', 'content-desc', 'checkable', 'checked', 'clickable', 'enabled', 'focusable', 'focused', 'scrollable', 'long-clickable', 'password', 'selected', 'bounds', 'midOf']
        rootNode = parseXML(testData)
        nodeList = parseXmlToList(rootNode)
        filtered = filterList(nodeList)
        for element in filtered:
            self.assertEqual(len(element), len(cols))
            self.assertTrue("midOf" in element)
            self.assertEqual(list(element.keys()), cols)

    def test_max_col_lengths(self):
        cols = ["resource-id", "text", "class", "bounds"]
        rootNode = parseXML(testData)
        nodeList = parseXmlToList(rootNode)
        filtered = filterList(nodeList, cols)
        max_cols = max_col_lengths(filtered)
        expected = [23, 232, 27, 20, 12]
        self.assertEqual(max_cols, expected)

    def test_clean_node(self):
        data = "com.balsdon.accessibilityDeveloperService:id/heading2"
        self.assertEqual(clean_node(data), "heading2")
        data2="Run \nadb shell settings put secure enabled_accessibility_services [service1]:[service2]"
        self.assertEqual(clean_node(data2), "Run adb shell settings put secure enabled_accessibility_services [service1]:[service2]")

    def test_pretty_print_line(self):
        cols = ["resource-id", "text", "class", "bounds"]
        rootNode = parseXML(testData)
        nodeList = [parseXmlToList(rootNode)[0]]
        filtered = filterList(nodeList, cols)
        max_cols = max_col_lengths(filtered)
        expected = "           |    |android.widget.FrameLayout|[0,0][1080,2160]|540.0 1080.0"
        self.assertEqual(pretty_print_line(list(filtered[0].values()), max_cols), expected)

    def test_validateArgs_none(self):
        array = validateArgs(None)
        self.assertEqual(array, None)

    def test_validateArgs_ignores_device_none(self):
        array = validateArgs(["-s", "SOME_DEVICE"])
        self.assertEqual(array, None)

    def test_validateArgs_ignores_device_success(self):
        array = validateArgs(["-s", "SOME_DEVICE", "resource-id", "text", "class", "bounds"])
        self.assertEqual(array, ["resource-id", "text", "class", "bounds"])

    def test_validateArgs_id_shorthand(self):
        array = validateArgs(["-s", "SOME_DEVICE", "id", "text", "class", "bounds"])
        self.assertEqual(array, ["resource-id", "text", "class", "bounds"])

if __name__ == "__main__":
    unittest.main()
