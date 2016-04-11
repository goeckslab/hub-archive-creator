#!/usr/bin/python
"""
This Galaxy tool permits to prepare your files to be ready for
Assembly Hub visualization.
Program test arguments:
hubArchiveCreator.py -g test-data/augustusDbia3.gff3 -f test-data/dbia3.fa -d . -u ./tools -o output.html
"""

import sys
import argparse

# Internal dependencies
from TrackHub import TrackHub
from AugustusProcess import AugustusProcess

# TODO: Verify each subprocessed dependency is accessible [gff3ToGenePred, genePredToBed, twoBitInfo, faToTwoBit, bedToBigBed, sort


def main(argv):
    # Command Line parsing init
    parser = argparse.ArgumentParser(description='Create a foo.txt inside the given folder.')

    parser.add_argument('-g', '--gff3', help='GFF3 output of Augustus')
    parser.add_argument('-f', '--fasta', help='Fasta file of the reference genome')

    # TODO: Check if the running directory can have issues if we run the tool outside
    parser.add_argument('-d', '--directory', help='Running tool directory, where to find the templates. Default is running directory')
    parser.add_argument('-u', '--ucsc_tools_path', help='Directory where to find the executables needed to run this tool')
    parser.add_argument('-e', '--extra_files_path', help='Name, in galaxy, of the output folder. Where you would want to build the Track Hub Archive')
    parser.add_argument('-o', '--output', help='Directory where to put the HTML summarizing the content of the Track Hub Archive')

    ucsc_tools_path = ''

    toolDirectory = '.'
    extra_files_path = '.'

    # Get the args passed in parameter
    args = parser.parse_args()

    inputGFF3File = args.gff3
    inputFastaFile = args.fasta
    outputFile = args.output

    if args.directory:
        toolDirectory = args.directory
    if args.extra_files_path:
        extra_files_path = args.extra_files_path
    if args.ucsc_tools_path:
        ucsc_tools_path = args.ucsc_tools_path

    # Create the Track Hub folder
    trackHub = TrackHub(inputFastaFile, extra_files_path, toolDirectory)

    # Process Augustus
    AugustusProcess(inputGFF3File, inputFastaFile, outputFile, toolDirectory, extra_files_path, ucsc_tools_path, trackHub)

    # We process all the modifications to create the zip file
    trackHub.createZip()

    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
