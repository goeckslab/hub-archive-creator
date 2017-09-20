#!/usr/bin/python
# -*- coding: utf8 -*-

"""
This Galaxy tool permits to prepare your files to be ready for
Assembly Hub visualization.
Program test arguments:
hubArchiveCreator.py -g test-data/augustusDbia3.gff3 -f '{"false_path": "./test-data/common/dbia3.fa", "name":"dbia3"}' -d . -u ./tools -o output.html
"""

import argparse
import collections
import json
import logging
import os
import sys

# Internal dependencies
from util.Reader import Reader
from util.Logger import Logger
from TrackHub import TrackHub



# TODO: Verify each subprocessed dependency is accessible [gff3ToGenePred, genePredToBed, twoBitInfo, faToTwoBit, bedToBigBed, sort


def main(argv):
    
    # Command Line parsing init
    parser = argparse.ArgumentParser(description='Create a foo.txt inside the given folder.')
    parser.add_argument('-j', '--data_json', help='JSON file containing the metadata of the inputs')
    parser.add_argument('-o', '--output', help='Name of the HTML summarizing the content of the Track Hub Archive')
    
    # Get the args passed in parameter
    args = parser.parse_args()
    json_inputs_data = args.data_json
    outputFile = args.output

    ##Parse JSON file with Reader
    reader = Reader(json_inputs_data)

    # Begin init variables
    extra_files_path = reader.getExtFilesPath()
    toolDirectory = reader.getToolDir()
    #outputFile = reader.getOutputDir()
    user_email = reader.getUserEmail()
    reference_genome = reader.getRefGenome()
    debug_mode = reader.getDebugMode()

    #### Logging management ####
    # If we are in Debug mode, also print in stdout the debug dump
    log = Logger(tool_directory=toolDirectory, debug=debug_mode, extra_files_path=extra_files_path)
    log.setup_logging()
    logging.info('#### HubArchiveCreator: Start ####\n')
    logging.debug('---- Welcome in HubArchiveCreator Debug Mode ----\n')
    logging.debug('JSON parameters: %s\n\n', json.dumps(reader.args))
    #### END Logging management ####

    # Create the Track Hub folder
    logging.info('#### HubArchiveCreator: Creating the Track Hub folder ####\n')
    trackHub = TrackHub(reference_genome, user_email, outputFile, extra_files_path, toolDirectory)

    # Create Ordered Dictionary to add the tracks in the tool form order
    logging.info('#### HubArchiveCreator: Preparing track data ####\n')
    all_datatype_dictionary = reader.getTracksData()
    all_datatype_ordered_dictionary = collections.OrderedDict(all_datatype_dictionary)

    logging.debug("----- End of all_datatype_dictionary processing -----")
    #logging.debug("all_datatype_ordered_dictionary are: %s", json.dumps(all_datatype_ordered_dictionary))

    logging.info('#### HubArchiveCreator: Adding tracks to Track Hub ####\n')
    logging.debug("----- Beginning of Track adding processing -----")

    for index, datatypeObject in all_datatype_ordered_dictionary.iteritems():
       trackHub.addTrack(datatypeObject.track.track_db)

    logging.debug("----- End of Track adding processing -----")

    # We terminate the process and so create a HTML file summarizing all the files
    logging.info('#### HubArchiveCreator: Creating the HTML file ####\n')
    trackHub.terminate()

    logging.debug('---- End of HubArchiveCreator Debug Mode: Bye! ----\n')
    logging.info('#### HubArchiveCreator: Congratulation! Assembly Hub is created! ####\n')

    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
