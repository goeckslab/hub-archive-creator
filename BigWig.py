#!/usr/bin/python

import os
import shutil

# Internal dependencies
from Track import Track
from util import subtools


class BigWig(object):
    def __init__( self, input_bigwig_path, input_fasta_path, extra_files_path ):
        super(BigWig, self).__init__()

        # Steps:
        #   1. If from Bam, convert it to BigWig:
        #       aa. sort bam: samtools sort $bam
        #       a. bedtools genomecov -bg -split -ibam $input -g $chromSizes
        #       b. bedGraphToBigWig temp.bg $chromSizes $output
        #   2. Add the bigwig file to os.path.join(mySpecieFolderPath, "tracks")

        # ======= Example from Bed ===========

        self.track = None

        self.input_bigwig_path = input_bigwig_path

        self.input_fasta_path = input_fasta_path

        self.extra_files_path = extra_files_path

        # Before the bedToBigBed processing, we need to retrieve the chrom.sizes file from the reference genome
        mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # 2bit file creation from input fasta
        self.twoBitFile = subtools.faToTwoBit(self.input_fasta_path, mySpecieFolderPath)

        myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "bigWig.bigwig"

        myBigWigFilePath = os.path.join(myTrackFolderPath, trackName)
        shutil.copy(self.input_bigwig_path, myBigWigFilePath)

        # Create the Track Object
        dataURL = "tracks/%s" % trackName

        # Return the BigBed track
        self.track = Track(
            trackFile=myBigWigFilePath,
            trackName=trackName,
            longLabel='From BigWig',
            shortLabel='BigWig file',
            trackDataURL=dataURL,
            trackType='bigWig',
            visibility='full')

        print("- %s created in %s" % (trackName, myBigWigFilePath))
