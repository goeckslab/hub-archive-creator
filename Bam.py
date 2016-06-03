#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Class to handle Bam files to UCSC TrackHub
"""

import os
import shutil

from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class Bam( Datatype ):
    def __init__( self, input_bam_false_path, data_bam ,
                 inputFastaFile, extra_files_path, tool_directory ):
        super(Bam, self).__init__( input_fasta_file=inputFastaFile,
                                   extra_files_path=extra_files_path,
                                   tool_directory=tool_directory)

        self.track = None

        self.input_bam_false_path = input_bam_false_path

        self.data_bam = data_bam
        # TODO: Check if it already contains the .bam extension / Do a function in Datatype which check the extension
        self.name_bam = self.data_bam["name"] + ".bam"
        self.index_bam = self.data_bam["index"]

        print "Creating TrackHub BAM from (falsePath: %s; name: %s)" % ( self.input_bam_false_path, self.name_bam)

        # First: Add the bam file
        # Second: Add the bam index file, in the same folder (https://genome.ucsc.edu/goldenpath/help/bam.html)

        bam_file_path = os.path.join(self.myTrackFolderPath, self.name_bam)
        shutil.copyfile(self.input_bam_false_path, bam_file_path)

        # Create and add the bam index file to the same folder
        name_index_bam = self.name_bam + ".bai"
        bam_index_file_path = os.path.join(self.myTrackFolderPath, name_index_bam)
        shutil.copyfile(self.index_bam, bam_index_file_path)

        # Create the Track Object
        dataURL = "tracks/%s" % self.name_bam

        trackDb = TrackDb(
            trackName=self.name_bam,
            longLabel='From Bam',  # TODO: Change this because it can be called by others thing that .bed => .gtf/.gff3
            shortLabel='bam file',
            trackDataURL=dataURL,
            trackType='bam',
            visibility='pack',
        )

        # Return the Bam Track Object
        self.track = Track(
            trackFile=bam_index_file_path,
            trackDb=trackDb,
        )

        print("- %s created in %s" % (self.name_bam, bam_file_path))
        print("- %s created in %s" % (self.index_bam, bam_index_file_path))
