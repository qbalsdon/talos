#!/usr/bin/env python3
from simplifier import setUp
from xml.etree.cElementTree import tostring as XmlToString

if __name__ == "__main__":
    options, xml = setUp(ui_required = True)
    print(XmlToString(xml))
