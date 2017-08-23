#!/usr/bin/python

import os
import tempfile

from Bed import Bed
from util import subtools


class BedSimpleRepeats( Bed ):
    def __init__(self, input_bed_simple_repeats_false_path, data_bed_simple_repeats):

        super(BedSimpleRepeats, self).__init__(input_bed_simple_repeats_false_path, data_bed_simple_repeats)
        self.bedType = "bed4+12"
        self.trackType = "bigBed 4 +"

    def convertBedTobigBed(self):
        # Sort processing
        self.sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        subtools.sort(self.inputBed, self.sortedBedFile.name)
        # bedToBigBed processing
        auto_sql_option = os.path.join(self.tool_directory, 'trf_simpleRepeat.as')
        with open(self.trackDataURL, 'w') as self.bigBedFile:
            subtools.bedToBigBed(self.sortedBedFile.name,
                                 self.chromSizesFile.name,
                                 self.bigBedFile.name,
                                 typeOption=self.bedType,
                                 tab='True',
                                 autoSql=auto_sql_option
                                 )
