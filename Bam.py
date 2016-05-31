#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Class to handle Bam files to UCSC TrackHub
"""

import os

from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class Bam( Datatype ):
    def __init__(self, inputBamFile, inputFastaFile, extra_files_path):
        super(Bam, self).__init__( input_fasta_file=inputFastaFile,
                                   extra_files_path=extra_files_path )

        self.track = None

        print "Creating TrackHub BAM from (falsePath: %s)" % ( inputBamFile )
        self.inputBamFile = inputBamFile

        # Temporary Files
        # Sorted Bed
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        sortedBam = "myBam.sorted.bam"

        # Created permanent files
        # Bam index file
        # TODO: Change the name depending on the inputs
        bamIndexFile = sortedBam + ".bai"

        # First: Add the bam file
        # Second: Add the bam index file, in the same folder (https://genome.ucsc.edu/goldenpath/help/bam.html)

        mySortedBamFilePath = os.path.join(self.myTrackFolderPath, sortedBam)
        with open(mySortedBamFilePath, 'w') as sortedBamPath:
            subtools.sortBam(self.inputBamFile, sortedBamPath.name)

        # Create and add the bam index file to the same folder
        bamIndexFilePath = os.path.join(self.myTrackFolderPath, bamIndexFile)
        print "bamIndexFilePath: %s" % bamIndexFilePath
        subtools.createBamIndex(mySortedBamFilePath, bamIndexFilePath)

        # Create the Track Object
        dataURL = "tracks/%s" % sortedBam

        trackDb = TrackDb(
            trackName=sortedBam,
            longLabel='From Bam',  # TODO: Change this because it can be called by others thing that .bed => .gtf/.gff3
            shortLabel='bam file',
            trackDataURL=dataURL,
            trackType='bam',
            visibility='pack',
        )

        # Return the Bam Track Object
        self.track = Track(
            trackFile=mySortedBamFilePath,
            trackDb=trackDb,
        )

        print("- %s created in %s" % (sortedBam, mySortedBamFilePath))
        print("- %s created in %s" % (bamIndexFile, bamIndexFilePath))
