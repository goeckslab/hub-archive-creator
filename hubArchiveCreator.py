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
import logging
import os
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

    parser.add_argument('--user_email', help='Email of the user who launched the Hub Archive Creation')

    parser.add_argument('--genome_name', help='UCSC Genome Browser assembly ID')

    parser.add_argument('--debug_mode', action='store_true', help='Allow more details about the errors')

    # Begin init variables

    toolDirectory = '.'
    extra_files_path = '.'

    # Get the args passed in parameter
    args = parser.parse_args()

    extra_files_path = args.extra_files_path
    toolDirectory = args.directory

    #### Logging management ####
    logging_level = logging.INFO
    log_format = '%(message)s'

    # .log configuration
    logging_file_path = os.path.join(extra_files_path, 'hac.log')

    # In any case, dump debug in the log
    logging.basicConfig(filename=logging_file_path, level=logging.DEBUG)

    # If we are in Debug mode, also print in stdout the debug dump
    if args.debug_mode is True:
        logging_level = logging.DEBUG

        # TODO: Give more info with this because we are debug?
        #log_format = '%(message)s'

    # stdout for logging to user configuration
    log_user = logging.StreamHandler(sys.stdout)
    log_user.setLevel(logging_level)

    formatter = logging.Formatter(log_format)

    log_user.setFormatter(formatter)

    logging.getLogger().addHandler(log_user)

    # stderr

    logging.debug('#### Welcome in HubArchiveCreator Debug Mode ####\n')
    #### END Logging management ####

    array_inputs_reference_genome = json.loads(args.fasta)

    # TODO: Replace these with the object Fasta
    input_fasta_file = array_inputs_reference_genome["false_path"]
    input_fasta_file_name = sanitize_name_input(array_inputs_reference_genome["name"])
    genome_name = sanitize_name_input(args.genome_name)

    reference_genome = Fasta(input_fasta_file,
                             input_fasta_file_name, genome_name)

    user_email = args.user_email


    # TODO: Use a class to have a better management of the structure of these inputs
    # These inputs are populated in the Galaxy Wrapper xml and are in this format:
    # ARRAY[DICT{FILE_PATH: DICT{NAME: NAME_VALUE, EXTRA_DATA: EXTRA_DATA_VALUE}}]
    # EXTRA_DATA could be anything, for example the index of a BAM => {"index", FILE_PATH}
    array_inputs_gff3 = args.gff3
    array_inputs_bed_simple_repeats = args.bedSimpleRepeats
    array_inputs_bed_generic = args.bed
    array_inputs_gtf = args.gtf
    array_inputs_bam = args.bam
    array_inputs_bigwig = args.bigwig

    outputFile = args.output

    json_inputs_data = args.data_json

    inputs_data = json.loads(json_inputs_data)
    # We remove the spaces in ["name"] of inputs_data
    sanitize_name_inputs(inputs_data)


    # TODO: Check here all the binaries / tools we need. Exception if missing

    # Create the Track Hub folder
    trackHub = TrackHub(reference_genome, user_email, outputFile, extra_files_path, toolDirectory)

    all_datatype_dictionary = {}

    for (inputs, datatype_class) in [(array_inputs_gff3, Gff3),
                         (array_inputs_bed_simple_repeats, BedSimpleRepeats),
                         (array_inputs_bed_generic, Bed),
                         (array_inputs_gtf, Gtf),
                         (array_inputs_bam, Bam),
                         (array_inputs_bigwig, BigWig)]:
        if inputs:
            all_datatype_dictionary.update(create_ordered_datatype_objects(datatype_class, inputs, inputs_data))

    # Create Ordered Dictionary to add the tracks in the tool form order
    all_datatype_ordered_dictionary = collections.OrderedDict(all_datatype_dictionary)

    for index, datatypeObject in all_datatype_ordered_dictionary.iteritems():
        trackHub.addTrack(datatypeObject.track.trackDb)

    # We process all the modifications to create the zip file
    #trackHub.createZip()

    # We terminate le process and so create a HTML file summarizing all the files
    trackHub.terminate()

    logging.debug('#### End of HubArchiveCreator Debug Mode: Bye! ####')

    sys.exit(0)


def sanitize_name_input(string_to_sanitize):
        return string_to_sanitize \
            .replace("/", "_") \
            .replace(" ", "_")


def sanitize_name_inputs(inputs_data):
    """
    Sometimes output from Galaxy, or even just file name from user have spaces
    Also, it can contain '/' character and could break the use of os.path function
    :param inputs_data: dict[string, dict[string, string]]
    :return:
    """
    for key in inputs_data:
        inputs_data[key]["name"] = sanitize_name_input(inputs_data[key]["name"])


def create_ordered_datatype_objects(ExtensionClass, array_inputs, inputs_data):
    """
    Function which executes the creation all the necessary files / folders for a special Datatype, for TrackHub
    and update the dictionary of datatype
    :param ExtensionClass: T <= Datatype
    :param array_inputs: list[string]
    :param inputs_data:
    """

    datatype_dictionary = {}

    # TODO: Optimize this double loop
    for input_false_path in array_inputs:
        for key, data_value in inputs_data.items():
            if key == input_false_path:
                extensionObject = ExtensionClass(input_false_path, data_value)
                datatype_dictionary.update({data_value["order_index"]: extensionObject})
    return datatype_dictionary

if __name__ == "__main__":
    main(sys.argv)
