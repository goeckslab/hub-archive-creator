#!/usr/bin/python
# -*- coding: utf8 -*-

"""
This Galaxy tool permits to prepare your files to be ready for
Assembly Hub visualization.
Program test arguments:
hubArchiveCreator.py -g test-data/augustusDbia3.gff3 -f test-data/dbia3.fa -d . -u ./tools -o output.html
"""

import argparse
import json
import sys

# Internal dependencies
from TrackHub import TrackHub
from AugustusProcess import AugustusProcess
from Bam import Bam
from BedSimpleRepeats import BedSimpleRepeats
from Bed import Bed
from BigWig import BigWig
from Gtf import Gtf


# TODO: Verify each subprocessed dependency is accessible [gff3ToGenePred, genePredToBed, twoBitInfo, faToTwoBit, bedToBigBed, sort


def main(argv):
    # Command Line parsing init
    parser = argparse.ArgumentParser(description='Create a foo.txt inside the given folder.')

    # Reference genome mandatory
    parser.add_argument('-f', '--fasta', help='Fasta file of the reference genome')

    # GFF3 Management
    parser.add_argument('-g', '--gff3', help='GFF3 output of Augustus')

    # GTF Management
    parser.add_argument('-z', '--gtf', help='GTF format')

    # Bed4+12 (TrfBig)
    parser.add_argument('-t', '--bedSimpleRepeats', help='Bed4+12 format, using simpleRepeats.as')

    # Generic Bed (Blastx transformed to bed)
    parser.add_argument('-b', '--bed', action='append', help='Bed generic format')

    # BigWig Management
    parser.add_argument('--bigwig', help='BigWig format')

    # Bam Management
    parser.add_argument('--bam', help='Bam format')

    # TODO: Check if the running directory can have issues if we run the tool outside
    parser.add_argument('-d', '--directory',
                        help='Running tool directory, where to find the templates. Default is running directory')
    parser.add_argument('-u', '--ucsc_tools_path',
                        help='Directory where to find the executables needed to run this tool')
    parser.add_argument('-e', '--extra_files_path',
                        help='Name, in galaxy, of the output folder. Where you would want to build the Track Hub Archive')
    parser.add_argument('-o', '--output', help='Name of the HTML summarizing the content of the Track Hub Archive')

    parser.add_argument('-j', '--data_json', help='Json containing the metadata of the inputs')

    ucsc_tools_path = ''

    toolDirectory = '.'
    extra_files_path = '.'

    # Get the args passed in parameter
    args = parser.parse_args()

    inputFastaFile = args.fasta

    # TODO: Add array for each input because we can add multiple -b for example + filter the data associated


    inputGFF3File = args.gff3
    inputBedSimpleRepeatsFile = args.bedSimpleRepeats
    array_inputs_bed_generic = args.bed
    inputGTFFile = args.gtf
    inputBamFile = args.bam
    input_bigWig_file_path = args.bigwig

    outputFile = args.output
    json_inputs_data = args.data_json

    inputs_data = json.loads(json_inputs_data)

    # TODO: Remove all spaces from the name in the dict
    # Sometimes output from Galaxy, or even just file name from user have spaces
    for key in inputs_data:
        inputs_data[key] = inputs_data[key].replace(" ", "_")

    if args.directory:
        toolDirectory = args.directory
    if args.extra_files_path:
        extra_files_path = args.extra_files_path
    if args.ucsc_tools_path:
        ucsc_tools_path = args.ucsc_tools_path

    # TODO: Check here all the binaries / tools we need. Exception is missing

    # Create the Track Hub folder
    trackHub = TrackHub(inputFastaFile, outputFile, extra_files_path, toolDirectory)

    # Process Augustus
    if inputGFF3File:
        augustusObject = AugustusProcess(inputGFF3File, inputFastaFile, outputFile, toolDirectory, extra_files_path,
                                         ucsc_tools_path, trackHub)
        trackHub.addTrack(augustusObject.track.trackDb)

    # Process Bed simple repeats => From Tandem Repeats Finder / TrfBig
    if inputBedSimpleRepeatsFile:
        bedRepeat = BedSimpleRepeats(inputBedSimpleRepeatsFile, inputFastaFile, outputFile, toolDirectory,
                                     extra_files_path, ucsc_tools_path, trackHub)
        trackHub.addTrack(bedRepeat.track.trackDb)

    # Process a Bed => tBlastN or TopHat
    # TODO: Optimize this double loop
    if array_inputs_bed_generic:
        for bed_path in array_inputs_bed_generic:
            for key, value in inputs_data.items():
                if key == bed_path:
                    bedGeneric = Bed(bed_path, value, inputFastaFile, extra_files_path)
                    trackHub.addTrack(bedGeneric.track.trackDb)

    # Process a GTF => Tophat
    if inputGTFFile:
        gtf = Gtf(inputGTFFile, inputFastaFile, extra_files_path)
        trackHub.addTrack(gtf.track.trackDb)

    # Process a Bam => Tophat
    if inputBamFile:
        bam = Bam(inputBamFile, inputFastaFile, extra_files_path)
        trackHub.addTrack(bam.track.trackDb)

    # Process a BigWig => From Bam
    if input_bigWig_file_path:
        bigWig = BigWig(input_bigWig_file_path, inputFastaFile, extra_files_path)
        trackHub.addTrack(bigWig.track)

    # We process all the modifications to create the zip file
    trackHub.createZip()

    # We terminate le process and so create a HTML file summarizing all the files
    trackHub.terminate()

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
