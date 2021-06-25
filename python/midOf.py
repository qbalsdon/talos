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
        raise ValueError("Required parameter(s) missing USAGE:"+midOf_usage)
    if "property" in options and "value" not in options:
        raise ValueError("Required '-v' parameter missing. USAGE:"+midOf_usage)
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
    numbers = re.findall('[0-9]+', foundNode.attrib.get("bounds"))
    if len(numbers) != 4:
        return None
    x = int(numbers[0]) + ((int(numbers[2]) - int(numbers[0])) / 2)
    y = int(numbers[1]) + ((int(numbers[3]) - int(numbers[1])) / 2)
    return {"x": x, "y": y}


if __name__ == "__main__":
    options = proccessArgs()
    getDevice(options=options)
    uiRoot = parseXML(options = options)
    print(midOf(options, uiRoot))
