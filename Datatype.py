#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Super Class of the managed datatype
"""

import os
import tempfile

from util import subtools


class Datatype(object):

    twoBitFile = None

    input_fasta_file = None
    extra_files_path = None
    tool_directory = None

    mySpecieFolderPath = None
    myTrackFolderPath = None

    twoBitFile = None
    chromSizesFile = None

    def __init__(self):

        not_init_message = "The {0} is not initialized." \
                           "Did you use pre_init static method first?"
        if Datatype.input_fasta_file is None:
            raise TypeError(not_init_message.format('reference genome'))
        if Datatype.extra_files_path is None:
            raise TypeError(not_init_message.format('track Hub path'))
        if Datatype.tool_directory is None:
            raise TypeError(not_init_message.format('tool directory'))


    @staticmethod
    def pre_init(reference_genome, two_bit_path, chrom_sizes_file,
                 extra_files_path, tool_directory, specie_folder, tracks_folder):
        Datatype.extra_files_path = extra_files_path
        Datatype.tool_directory = tool_directory

        # TODO: All this should be in TrackHub and not in Datatype
        Datatype.mySpecieFolderPath = specie_folder
        Datatype.myTrackFolderPath = tracks_folder

        Datatype.input_fasta_file = reference_genome

        # 2bit file creation from input fasta
        Datatype.twoBitFile = two_bit_path
        Datatype.chromSizesFile = chrom_sizes_file

    @staticmethod
    def get_largest_scaffold_name(self):
        # We can get the biggest scaffold here, with chromSizesFile
        with open(Datatype.chromSizesFile.name, 'r') as chrom_sizes:
            # TODO: Check if exists
            return chrom_sizes.readline().split()[0]

    # TODO: Rename for PEP8
    def getShortName( self, name_to_shortify ):
        # Slice to get from Long label the short label
        short_label_slice = slice(0, 15)

        return name_to_shortify[short_label_slice]
