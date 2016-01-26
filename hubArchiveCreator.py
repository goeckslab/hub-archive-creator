#! python
"""
This Galaxy tool permits to prepare your files to be ready for
Assembly Hub visualization.
"""

import sys
import tempfile
import getopt
import zipfile
import subprocess
import os

# Internal dependencies
from twoBitCreator import twoBitFileCreator


def main(argv):
    inputGFF3File = ''
    inputFastaFile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,
            "hg:f:o:",
            ['help',
            'gff3=',
            'fasta=',
            'output='])
    except getopt.GetoptError:
        # TODO: Modify
        print 'hubArchiveCreator.py -if <inputFastaFile> -ig <inputGFF3File> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', 'help'):
            # TODO: Modify
            print 'test.py -if <inputFastaFile> -ig <inputGFF3File> -o <outputfile>'
            sys.exit()
        elif opt in ("-g", 'gff3'):
            # We retrieve the input file
            inputGFF3File = open(arg, 'r')
        elif opt in ("-f", 'fasta'):
            # We retrieve the input file
            inputFastaFile = open(arg, 'r')
        elif opt in ("-o", 'output'):
            outputZip = zipfile.ZipFile(arg, 'w')

            # TODO: See if we need these temporary files as part of the generated files
            genePredFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
            unsortedBedFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsortedBed")
            sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
            bigBedFile = tempfile.NamedTemporaryFile(suffix=".bb")

            # gff3ToGenePred processing
            print inputGFF3File.name
            p = subprocess.Popen(
                ['tools/gff3ToGenePred',
                    inputGFF3File.name,
                    genePredFile.name])
            # We need to wait the time gff3ToGenePred terminate so genePredToBed can begin
            # TODO: Check if we should use communicate instead of wait
            p.wait()

            # genePredToBed processing
            p = subprocess.Popen(
                ['tools/genePredToBed',
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

            # 2bit file creation from input fasta
            twoBitFile = twoBitFileCreator(inputFastaFile)

            # bedToBigBed processing
            # bedToBigBed processing
            # p = subprocess.Popen(
            #    ['Tools/bedToBigBed',
            #        sortedBedFile.name,
            #        bigBedFile.name])
            # p.wait()

            outputZip.write(sortedBedFile.name)
            outputZip.write(twoBitFile.name)
            outputZip.close()

if __name__ == "__main__":
    main(sys.argv[1:])
