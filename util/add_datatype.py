#!/usr/bin/python

"""
This script copy the huba datatype into your galaxy:
    - Add under <registration>, the datatype_conf
    - Add huba.xml under display_application/ucsc/
    - Add hubAssembly.py inside lib/galaxy/datatypes
Place yourself in the folder of the python script, and launch it
- Based on the fact datatypes_conf
"""

import argparse
import os
import shutil
import sys
import xml.etree.ElementTree as ET


def main(argv):
    # Command Line parsing init
    parser = argparse.ArgumentParser(description='Create a foo.txt inside the given folder.')

    parser.add_argument('-g', '--galaxy_root', help='Galaxy root folder', required=True)

    # Get the args passed in parameter
    args = parser.parse_args()

    galaxy_root_path = args.galaxy_root

    add_datatype_conf(galaxy_root_path)
    add_huba_xml(galaxy_root_path)
    add_hubAssembly(galaxy_root_path)


def add_datatype_conf(galaxy_root_path):
    print "======= Add datatype ======="
    datatype_conf_path = os.path.join(galaxy_root_path, 'config/datatypes_conf.xml')
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

    huba_datatype = ET.parse('../hubaDataType/datatypes_conf.xml').getroot()
    # TODO: Verify the datatype is not already existing, else do not add / write. And in another version, check it
    registration.append(huba_datatype)
    tree.write(datatype_conf_path)
    print "datatype added in %s" % datatype_conf_path
    return


def add_huba_xml(galaxy_root_path):
    print "======= Add hub xml ======="
    displayApp_ucsc_path = os.path.join(galaxy_root_path, "display_applications/ucsc/")
    shutil.copy("../hubaDataType/huba.xml", displayApp_ucsc_path)
    print "Content of %s now: %s" % (displayApp_ucsc_path, os.listdir(displayApp_ucsc_path))
    return


def add_hubAssembly(galaxy_root_path):
    print "======= Add hubAssembly ======="
    datatype_lib_path = os.path.join(galaxy_root_path, "lib/galaxy/datatypes/")
    shutil.copy("../hubaDataType/hubAssembly.py", datatype_lib_path)
    print "Content of %s now: %s" % (datatype_lib_path, os.listdir(datatype_lib_path))
    return


if __name__ == "__main__":
    main(sys.argv)
