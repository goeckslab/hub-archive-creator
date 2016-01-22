#! python
"""
This Galaxy tool permits to prepare your files to be ready for
Assembly Hub visualization.
"""

import sys
import getopt
import zipfile
import subprocess


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'hubArchiveCreator.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            # We retrieve the input file
            inputfile = open(arg, 'r')
        elif opt in ("-o", "--ofile"):
            inputfile = open(arg, 'w+')
            subprocess.Popen(
                ['Tools/gff3ToGenePred',
                    inputfile.name,
                    outputfile.name])

if __name__ == "__main__":
    main(sys.argv[1:])
