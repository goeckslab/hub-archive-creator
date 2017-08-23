#!/usr/bin/python

import os
import tempfile

from Bed import Bed
from util import subtools


class BedSpliceJunctions( Bed ):
    def __init__(self, input_bed_splice_junctions_false_path, data_bed_splice_junctions):

        super(BedSpliceJunctions, self).__init__(input_bed_splice_junctions_false_path, data_bed_splice_junctions)
        self.bedType = "bed12+1"
        self.trackType = "bigBed 12 +"

    def convertBedTobigBed(self):
        # Sort processing
        self.sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        subtools.sort(self.inputBed, self.sortedBedFile.name)
        # bedToBigBed processing
        auto_sql_option = os.path.join(self.tool_directory, 'spliceJunctions.as')
        with open(self.trackDataURL, 'w') as self.bigBedFile:
            subtools.bedToBigBed(self.sortedBedFile.name,
                                 self.chromSizesFile.name,
                                 self.bigBedFile.name,
                                 typeOption=self.bedType,
                                 tab='True',
                                 autoSql=auto_sql_option
                                 )