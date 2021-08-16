#!/usr/bin/env python3
import sys
from simplifier import setUp, parseXML
from midOf import midOfBounds
import os, re
from xml.etree.cElementTree import tostring as XmlToString

def validateArgs(arguments):
    if arguments == None:
        return None
    if len(arguments) > 0:
        if "-s" in arguments:
            pos = arguments.index("-s")
            del arguments[pos + 1]
            arguments.remove("-s")
    if len(arguments) == 0:
        return None

    if "id" in arguments:
        arguments[arguments.index("id")] = "resource-id"

    return arguments

def parseXmlToList(xmlNode):
    elementList = []
    for node in xmlNode.findall(f".//node"):
        node.attrib.pop("index")
        elementList = elementList + [node.attrib]
    return elementList

def clean_node(data):
    return re.sub(r'^.*?/', '', data).replace("\n","")

def filterList(nodeList, colList=None):
    result = []

    if colList == None:
        colList = list(nodeList[0].keys())

    for node in nodeList:
        nElement = {}
        for col in colList:
            if col in node:
                nElement[col] = clean_node(node[col])
            else:
                nElement[col] = '-'

        mid = midOfBounds(node["bounds"])
        nElement["midOf"] = str(mid["x"]) + " " + str(mid["y"])

        result = result + [nElement]

    return result

def max_col_lengths(elements):
    result = [len(key) for key in elements[0]] # titles are the base length
    for node in elements:
        for index in range(len(node)):
            value_at_index = list(node.values())[index]
            if len(value_at_index) > result[index]:
                result[index] = len(value_at_index)
    return result

def pretty_print_line(elementAsList, lengths):
    result = None
    for index in range(len(lengths)):
        value_at_index = str(elementAsList[index]).ljust(lengths[index], ' ')
        if result != None:
            result = result + "|" + value_at_index
        else:
            result = value_at_index
    return result

def pretty_print(elements):
    lengths = max_col_lengths(elements)
    result = pretty_print_line(list(elements[0].keys()), lengths)
    for node in elements:
        result = result + "\n" + pretty_print_line(list(node.values()), lengths)
    return result

if __name__ == "__main__":
    options, uiRoot = setUp()
    args = sys.argv
    del args[0]
    headings = validateArgs(args)
    print(pretty_print(filterList(parseXmlToList(uiRoot), headings)))
