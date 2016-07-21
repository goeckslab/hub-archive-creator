#!/usr/bin/python
# -*- coding: utf8 -*-

"""
This Galaxy tool permits to prepare your files to be ready for
Assembly Hub visualization.
Program test arguments:
hubArchiveCreator.py -g test-data/augustusDbia3.gff3 -f test-data/dbia3.fa -d . -u ./tools -o output.html
"""

import argparse
import collections
import json
import sys

# Internal dependencies
from Bam import Bam
from BedSimpleRepeats import BedSimpleRepeats
from Bed import Bed
from BigWig import BigWig
from util.Fasta import Fasta
from Gff3 import Gff3
from Gtf import Gtf
from TrackHub import TrackHub


# TODO: Verify each subprocessed dependency is accessible [gff3ToGenePred, genePredToBed, twoBitInfo, faToTwoBit, bedToBigBed, sort


def main(argv):
    # Command Line parsing init
    parser = argparse.ArgumentParser(description='Create a foo.txt inside the given folder.')

    # Reference genome mandatory
    parser.add_argument('-f', '--fasta', help='Fasta file of the reference genome')

    # GFF3 Management
    parser.add_argument('--gff3', action='append', help='GFF3 format')

    # GTF Management
    parser.add_argument('--gtf', action='append', help='GTF format')

    # Bed4+12 (TrfBig)
    parser.add_argument('--bedSimpleRepeats', action='append', help='Bed4+12 format, using simpleRepeats.as')

    # Generic Bed (Blastx transformed to bed)
    parser.add_argument('--bed', action='append', help='Bed generic format')

    # BigWig Management
    parser.add_argument('--bigwig', action='append', help='BigWig format')

    # Bam Management
    parser.add_argument('--bam', action='append', help='Bam format')

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

    array_inputs_reference_genome = json.loads(args.fasta)
    reference_genome = Fasta(array_inputs_reference_genome["false_path"], array_inputs_reference_genome["name"])

    # TODO: Replace these with the object Fasta
    input_fasta_file = array_inputs_reference_genome["false_path"]
    input_fasta_file_name = array_inputs_reference_genome["name"]

    # TODO: Add array for each input because we can add multiple -b for example + filter the data associated


    array_inputs_gff3 = args.gff3
    array_inputs_bed_simple_repeats = args.bedSimpleRepeats
    array_inputs_bed_generic = args.bed
    array_inputs_gtf = args.gtf
    array_inputs_bam = args.bam
    array_inputs_bigwig = args.bigwig

    outputFile = args.output
    json_inputs_data = args.data_json

    json_inputs_data = args.data_json

    inputs_data = json.loads(json_inputs_data)
    # We remove the spaces in ["name"] of inputs_data
    sanitize_name_inputs(inputs_data)

    if args.directory:
        toolDirectory = args.directory
    if args.extra_files_path:
        extra_files_path = args.extra_files_path

    # TODO: Check here all the binaries / tools we need. Exception if missing

    # Create the Track Hub folder
    trackHub = TrackHub(input_fasta_file, outputFile, extra_files_path, toolDirectory)

    all_datatype_dictionary = {}

    # Process Augustus
    if array_inputs_gff3:
        create_ordered_datatype_objects(Gff3, array_inputs_gff3, inputs_data, input_fasta_file,
                                        extra_files_path, all_datatype_dictionary, toolDirectory)

    # Process Bed simple repeats => From Tandem Repeats Finder / TrfBig
    if array_inputs_bed_simple_repeats:
        create_ordered_datatype_objects(BedSimpleRepeats, array_inputs_bed_simple_repeats, inputs_data, input_fasta_file,
                                        extra_files_path, all_datatype_dictionary, toolDirectory)

    # Process a Bed => tBlastN or TopHat
    if array_inputs_bed_generic:
        create_ordered_datatype_objects(Bed, array_inputs_bed_generic, inputs_data, input_fasta_file,
                                        extra_files_path, all_datatype_dictionary, toolDirectory)

    # Process a GTF => Tophat
    if array_inputs_gtf:
        create_ordered_datatype_objects(Gtf, array_inputs_gtf, inputs_data, input_fasta_file,
                                        extra_files_path, all_datatype_dictionary, toolDirectory)

    # Process a Bam => Tophat
    if array_inputs_bam:
        create_ordered_datatype_objects(Bam, array_inputs_bam, inputs_data, input_fasta_file,
                                        extra_files_path, all_datatype_dictionary, toolDirectory)

    # Process a BigWig => From Bam
    if array_inputs_bigwig:
        create_ordered_datatype_objects(BigWig, array_inputs_bigwig, inputs_data, input_fasta_file,
                                        extra_files_path, all_datatype_dictionary, toolDirectory)

    # Create Ordered Dictionary to add the tracks in the tool form order
    all_datatype_ordered_dictionary = collections.OrderedDict(all_datatype_dictionary)

    for index, datatypeObject in all_datatype_ordered_dictionary.iteritems():
        trackHub.addTrack(datatypeObject.track.trackDb)

    # We process all the modifications to create the zip file
    #trackHub.createZip()

    # We terminate le process and so create a HTML file summarizing all the files
    trackHub.terminate()

    sys.exit(0)


def sanitize_name_inputs(inputs_data):
    """
    Sometimes output from Galaxy, or even just file name from user have spaces
    Also, it can contain '/' character and could break the use of os.path function
    :param inputs_data: dict[string, dict[string, string]]
    :return:
    """
    for key in inputs_data:
        inputs_data[key]["name"] = inputs_data[key]["name"]\
            .replace("/", "_")\
            .replace(" ", "_")


def create_ordered_datatype_objects(ExtensionClass, array_inputs, inputs_data, input_fasta_file,
                                    extra_files_path, all_datatype_dictionary, tool_directory):
    """
    Function which executes the creation all the necessary files / folders for a special Datatype, for TrackHub
    and update the dictionary of datatype
    :param ExtensionClass: T <= Datatype
    :param array_inputs: list[string]
    :param inputs_data:
    :param input_fasta_file: string
    :param extra_files_path: string
    :param tool_directory; string
    """

    datatype_dictionary = {}

    # TODO: Optimize this double loop
    for input_false_path in array_inputs:
        for key, data_value in inputs_data.items():
            if key == input_false_path:
                extensionObject = ExtensionClass(input_false_path, data_value,
                                                 input_fasta_file, extra_files_path, tool_directory)
                datatype_dictionary.update({data_value["order_index"]: extensionObject})
    all_datatype_dictionary.update(datatype_dictionary)

if __name__ == "__main__":
    main(sys.argv)
