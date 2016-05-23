"""
Class to handle Bam files to UCSC TrackHub
"""

import tempfile
import os

from Track import Track
from util import subtools

class Bam( object ):
    def __init__( self, inputBamFile, inputFastaFile ):
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
        bamIndexFile = "bai.bai"

        # Construction of the arborescence
        # TODO: Change the hard-coded path with a input based one
        mySpecieFolderPath = os.path.join("myHub", "dbia3")

        # TODO: Refactor the name of the folder "tracks" into one variable, and should be inside TrackHub object
        myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")

        # First: Add the bam file
        # Second: Add the bam index file, in the same folder (https://genome.ucsc.edu/goldenpath/help/bam.html)

        myBamFilePath = os.path.join(myTrackFolderPath, sortedBam)
        with open(myBamFilePath, 'w') as bamFile:
            subtools.sortBam(self.inputBamFile.name, sortedBam.name)

        # Create the Track Object
        dataURL = "tracks/%s" % sortedBam.name

        # Return the BigBed Track Object
        self.track = Track(
            trackFile=myBamFilePath,
            trackName=sortedBam.name,
            longLabel='From Bam',  # TODO: Change this because it can be called by others thing that .bed => .gtf/.gff3
            shortLabel='bam file',
            trackDataURL=dataURL,
            trackType='ban',
            visibility='display_mode')

        # Create and add the bam index file to the same folder
        bamIndexFilePath = os.path.join(myTrackFolderPath, bamIndexFile)
        subtools.createBamIndex(sortedBam.name, bamIndexFilePath)

        print("- %s created in %s" % (sortedBam.name, myBamFilePath))
        print("- %s created in %s" % (bamIndexFile.name, bamIndexFilePath))


