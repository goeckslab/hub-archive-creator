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
            outputfile = open(arg, 'w+')

            genePredFile = open('temp.genepred', 'w+')
            unsortedBedFile = open('temp.unsortedBed', 'w+')
            sortedBedFile = open('temp.sortedBed', 'w+')
            bigBedFile = open('temp.bb', 'w+')

            # gff3ToGenePred processing
            p = subprocess.Popen(
                ['Tools/gff3ToGenePred',
                    inputfile.name,
                    genePredFile.name])
            # We need to wait the time gff3ToGenePred terminate so genePredToBed can begin
            # TODO: Check if we should use communicate instead of wait
            p.wait()

            # genePredToBed processing
            p = subprocess.Popen(
                ['Tools/genePredToBed',
                    genePredFile.name,
                    unsortedBedFile.name])
            p.wait()

            # Sort processing
            p = subprocess.Popen(
                ['sort',
                    '-k'
                    '1,1',
                    '-k'
                    '2,2n',
                    unsortedBedFile.name,
                    '-o',
                    sortedBedFile.name])
            p.wait()

            # bedToBigBed processing
            p = subprocess.Popen(
                ['Tools/bedToBigBed',
                    sortedBedFile.name,
                    bigBedFile.name])
            p.wait()

if __name__ == "__main__":
    main(sys.argv[1:])
