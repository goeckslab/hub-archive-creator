#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Class to handle Bam files to UCSC TrackHub
"""

import os

from Track import Track
from util import subtools


class Bam( object ):
    def __init__( self, inputBamFile, inputFastaFile, extra_files_path ):
        super( Bam, self).__init__()

        self.track = None

        self.inputBamFile = inputBamFile
        self.inputFastaFile = inputFastaFile

        # Temporary Files
        # Sorted Bed
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        sortedBam = "myBam.sorted.bam"

        # Created permanent files
        # Bam index file
        # TODO: Change the name depending on the inputs
        bamIndexFile = sortedBam + ".bai"

        # Construction of the arborescence
        # TODO: Change the hard-coded path with a input based one
        mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")
        # TODO: Care about Race Condition + Move this in an util function
        # if not os.path.exists(mySpecieFolderPath):
        #     os.makedirs(mySpecieFolderPath)

        # TODO: Refactor the name of the folder "tracks" into one variable, and should be inside TrackHub object
        myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        # TODO: Care about Race Condition + Move this in an util function
        # if not os.path.exists(myTrackFolderPath):
        #     os.makedirs(myTrackFolderPath)

        # TODO: Redundant, should be refactored because they are all doing it...into hubArchiveCreator?
        # 2bit file creation from input fasta
        self.twoBitFile = subtools.faToTwoBit(self.inputFastaFile, mySpecieFolderPath)

        # First: Add the bam file
        # Second: Add the bam index file, in the same folder (https://genome.ucsc.edu/goldenpath/help/bam.html)

        mySortedBamFilePath = os.path.join(myTrackFolderPath, sortedBam)
        with open(mySortedBamFilePath, 'w') as sortedBamPath:
            subtools.sortBam(self.inputBamFile, sortedBamPath.name)

        # Create the Track Object
        dataURL = "tracks/%s" % sortedBam

        # Return the BigBed Track Object
        self.track = Track(
            trackFile=mySortedBamFilePath,
            trackName=sortedBam,
            longLabel='From Bam',  # TODO: Change this because it can be called by others thing that .bed => .gtf/.gff3
            shortLabel='bam file',
            trackDataURL=dataURL,
            trackType='bam',
            visibility='pack')

        # Create and add the bam index file to the same folder
        bamIndexFilePath = os.path.join(myTrackFolderPath, bamIndexFile)
        subtools.createBamIndex(mySortedBamFilePath, bamIndexFilePath)

        print("- %s created in %s" % (sortedBam, mySortedBamFilePath))
        print("- %s created in %s" % (bamIndexFile, bamIndexFilePath))
