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
    def __init__(self, input_bam_false_path, data_bam):
        super(Bam, self).__init__()

        self.track = None

        self.input_bam_false_path = input_bam_false_path

        self.data_bam = data_bam
        # TODO: Check if it already contains the .bam extension / Do a function in Datatype which check the extension
        if ".bam" not in self.data_bam["name"]:
            self.name_bam = self.data_bam["name"] + ".bam"
        else:
            self.name_bam = self.data_bam["name"]

        self.priority = self.data_bam["order_index"]
        self.index_bam = self.data_bam["index"]

        #print "Creating TrackHub BAM from (falsePath: %s; name: %s)" % ( self.input_bam_false_path, self.name_bam)

        # First: Add the bam file
        # Second: Add the bam index file, in the same folder (https://genome.ucsc.edu/goldenpath/help/bam.html)

        bam_file_path = os.path.join(self.myTrackFolderPath, self.name_bam)
        shutil.copyfile(self.input_bam_false_path, bam_file_path)

        # Create and add the bam index file to the same folder
        name_index_bam = self.name_bam + ".bai"
        bam_index_file_path = os.path.join(self.myTrackFolderPath, name_index_bam)
        shutil.copyfile(self.index_bam, bam_index_file_path)

        # Create the Track Object
        self.createTrack(file_path=self.name_bam,
                         track_name=self.name_bam,
                         long_label=self.name_bam, track_type='bam', visibility='pack', priority=self.priority,
                         track_file=bam_index_file_path)
        #
        # dataURL = "tracks/%s" % self.name_bam
        #
        # trackDb = TrackDb(
        #     trackName=self.name_bam,
        #     longLabel=self.name_bam,
        #     shortLabel=self.getShortName( self.name_bam ),
        #     trackDataURL=dataURL,
        #     trackType='bam',
        #     visibility='pack',
        #     priority=self.priority,
        # )
        #
        # # Return the Bam Track Object
        # self.track = Track(
        #     trackFile=bam_index_file_path,
        #     trackDb=trackDb,
        # )

        #print("- %s created in %s" % (self.name_bam, bam_file_path))
        #print("- %s created in %s" % (self.index_bam, bam_index_file_path))
