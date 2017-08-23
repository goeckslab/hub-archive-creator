#!/usr/bin/python

import os
import tempfile
import string

from Bed import Bed
from util import subtools


class BedBlastAlignments( Bed ):
    def __init__(self, input_bed_blast_alignments_false_path, data_bed_blast_alignments):

        super(BedBlastAlignments, self).__init__(input_bed_blast_alignments_false_path, data_bed_blast_alignments)
        self.bedType ='bed12+12'
        self.trackType = "bigBed 12 +"
    
    def initBedSettings(self):  
        super(BedBlastAlignments, self).initBedSettings()
        if "database" in self.bedMetaData:
            self.extra_settings["database"] = self.bedMetaData["database"]
    
    def convertBedTobigBed(self):
        # Sort processing
        self.sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        subtools.sort(self.inputBed, self.sortedBedFile.name)
        # bedToBigBed processing
        auto_sql_option = os.path.join(self.tool_directory, 'bigPsl.as')
        with open(self.trackDataURL, 'w') as self.bigBedFile:
            subtools.bedToBigBed(self.sortedBedFile.name,
                                 self.chromSizesFile.name,
                                 self.bigBedFile.name,
                                 typeOption=self.bedType,
                                 tab='True',
                                 autoSql=auto_sql_option,
                                 extraIndex='name'
                                 )
       
