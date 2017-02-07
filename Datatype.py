#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Super Class of the managed datatype
"""

import os
import tempfile

from util import subtools
from Track import Track
from TrackDb import TrackDb


class Datatype(object):

    twoBitFile = None

    input_fasta_file = None
    extra_files_path = None
    tool_directory = None

    mySpecieFolderPath = None
    myTrackFolderPath = None

    twoBitFile = None
    chromSizesFile = None

    track = None

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

    # TODO: Better handle parameters, use heritance mecanism
    # TODO: Use default parameters for some, like visibility
    def createTrack(self,
                    file_path=None,
                    track_name=None, long_label=None, thick_draw_item='off',
                    short_label=None, track_type=None, visibility=None, priority=None,
                    track_file=None, track_color='#000000', group_name="Default"):

        # TODO: Remove the hardcoded "tracks" by the value used as variable from myTrackFolderPath
        data_url = "tracks/%s" % file_path

        if not short_label:
            short_label = self.getShortName(long_label)

        # Replace '_' by ' ', to invert the sanitization mecanism
        # TODO: Find a better way to manage the sanitization of file path
        long_label = long_label.replace("_", " ")
        short_label = short_label.replace("_", " ")

        #TODO: Check if rgb or hexa
        # Convert hexa to rgb array
        hexa_without_sharp = track_color.lstrip('#')
        rgb_array = [int(hexa_without_sharp[i:i+2], 16) for i in (0, 2, 4)]
        rgb_ucsc = ','.join(map(str, rgb_array))

        #sanitize the track_name
        sanitized_name = subtools.fixName(track_name)
        
        track_db = TrackDb(
                trackName=sanitized_name,
                longLabel=long_label,
                shortLabel=short_label,
                trackDataURL=data_url,
                trackType=track_type,
                visibility=visibility,
                thickDrawItem=thick_draw_item,
                priority=priority,
                track_color=rgb_ucsc,
                group_name=group_name
        )

        # Return the Bam Track Object
        self.track = Track(
                trackFile=track_file,
                trackDb=track_db,
        )
