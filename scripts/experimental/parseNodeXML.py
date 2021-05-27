#Import required library
import xml.etree.cElementTree as ET

def parseXML(file_name):
   # Parse XML with ElementTree
   tree = ET.ElementTree(file=file_name)
   print(tree.getroot())
   root = tree.getroot()

   print("Iterating [%s]" % root.tag)

   rootNode = root.findall(f".//node")

   for node in rootNode:
      print("    %s: %s" % (node.tag, node.attrib.get("bounds")))

if __name__ == "__main__":
   parseXML("/Users/quba/Sandbox/test.xml")
