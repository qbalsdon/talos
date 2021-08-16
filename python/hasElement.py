#!/usr/bin/env python3
import sys
from simplifier import setUp
from xml.etree.cElementTree import tostring as XmlToString

hasElement_usage = "hasElement.py [-s DEVICE] [attribute:value] [attribute:value] ..."

def validateArgs(arguments):
    if arguments == None:
        raise ValueError("No attribute:value pairs given.\nUsage:\n" + hasElement_usage)
    if len(arguments) > 0:
        if "-s" in arguments:
            pos = arguments.index("-s")
            del arguments[pos + 1]
            arguments.remove("-s")
    if len(arguments) == 0:
        raise ValueError("No attribute:value pairs given.\nUsage:\n" + hasElement_usage)

    result = {}
    for argument in arguments:
        elements = argument.split(":")
        if len(elements) != 2:
            raise ValueError("Invalid attribute:value pair: " + arguments + "\nUsage:\n" + hasElement_usage)
        if "id" in elements:
            elements[elements.index("id")] = "resource-id"
        result[elements[0]] = elements[1]
    return result

def findMatchingElements(rootNode, elementMap):
    elementList = []
    for node in rootNode.findall(f".//node"):
        isAMatch = True
        for key in elementMap:
            isAMatch = isAMatch and key in node.attrib and elementMap[key] in node.attrib[key]
            if not isAMatch:
                break
        if isAMatch:
            elementList = elementList + [node]
    return elementList

if __name__ == "__main__":
    options, uiRoot = setUp()
    args = sys.argv
    del args[0]
    searchCriteria = validateArgs(args)
    print(len(findMatchingElements(uiRoot, searchCriteria)) > 0)
