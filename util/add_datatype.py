#!/usr/bin/python

"""
This script copy the huba datatype into your galaxy:
    - Add under <registration>, the datatype_conf
    - Add huba.xml under display_application/ucsc/
    - Add hubAssembly.py inside lib/galaxy/datatypes
Place yourself in the folder of the python script, and launch it
- Based on the fact datatypes_conf
"""

import sys
import xml.etree.ElementTree as ET

def main(argv):
    add_datatype_conf()
    add_huba_xml()
    add_hubAssembly()

def add_datatype_conf():
    print "Add datatype"
    datatype_conf_path = '../../../config/datatypes_conf.xml'
    # TODO: Not relative to this python file but based on a parameter galaxy_root
    # TODO: Check if datatypes_conf.xml, if not create it by copying datatypes_conf.xml.sample
    # TODO: For debug only
    # tree = ET.parse('../test-data/add_datatype/datatypes_conf.xml.sample')
    # TODO: UnComment for prod
    tree = ET.parse(datatype_conf_path)
    root = tree.getroot()
    print root.tag
    registration = root[0]
    print registration.attrib

    huba_datatype = ET.parse('../hubaDatatype/datatypes_conf.xml').getroot()
    registration.append(huba_datatype)
    tree.write(datatype_conf_path)
    print "datatype added in %s" % datatype_conf_path
    return

def add_huba_xml():
    print "Add hub xml"
    return

def add_hubAssembly():
    print "Add hubAssembly"
    return

if __name__ == "__main__":
    main(sys.argv)