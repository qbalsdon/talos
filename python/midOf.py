#!/usr/bin/env python3
from common import *
from deviceManager import *
from fetchUI import *

midOf_usage="""
  midOf [-s DEVICE] [-f|-x XML_RESOURCE]
       -e ELEMENT_MATCHER |
       -prop ELEMENT_PROPERTY -v ELEMENT_PROPERT_VALUE
"""

def validateArgs(options):
    if options == None or "element" not in options and "property" not in options:
        print("Required parameter(s) missing USAGE:"+midOf_usage)
        return False
    if "property" in options and "value" not in options:
        print("Required '-v' parameter missing. USAGE:"+midOf_usage)
        return False
    return True

def midOf(options, uiRoot):
    if not validateArgs(options):
        return None
    searchStr = './/node'
    foundNode = None

    if "element" in options:
        lowerSearch = options.get("element").lower()
        for node in uiRoot.findall(searchStr):
            if any(lowerSearch in elem.lower() for elem in node.attrib.values()):
                foundNode = node
                break

    if "property" in options:
        searchProp  = options.get("property")
        lowerSearchValue = options.get("value").lower()
        for node in uiRoot.findall(searchStr):
            if searchProp in node.attrib.keys() and lowerSearchValue in node.attrib.get(searchProp).lower():
                foundNode = node
                break

    if foundNode == None:
        return None
    numbers = re.findall('[0-9]+', node.attrib.get("bounds"))
    if len(numbers) != 4:
        return None
    x = int(numbers[2]) - int(numbers[0])
    y = int(numbers[3]) - int(numbers[1])
    return {"x": x, "y": y}


if __name__ == "__main__":
    options = proccessArgs()
    uiRoot = parseXML(options = options)
    print(midOf(options, uiRoot))
