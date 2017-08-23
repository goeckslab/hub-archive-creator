#!/usr/bin/python

import os
import tempfile
import string

from Bed import Bed
from Track import Track
from TrackDb import TrackDb
from util import subtools


class BedBlastAlignments(Bed):
    def __init__(self, input_bed_blast_alignments_false_path, data_bed_blast_alignments):

        super(BedBlastAlignments, self).__init__(input_bed_blast_alignments_false_path, data_bed_blast_alignments)
        self.bedType ='bed12+12'
       # self.initBedSettings(self.bedMetaData, 'bed12+12')
       # self.convertBedTobigBed()
       # self.createTrack(trackName=self.trackName,
       #                  longLabel=self.longLabel, 
       #                  shortLabel=self.shortLabel,
       #                  trackDataURL=self.trackDataURL,
       #                  trackType=self.trackType,
       #                  extra_settings = self.extra_settings)

        

    ''' 
        self.input_bed_blast_alignments_false_path = input_bed_blast_alignments_false_path
        self.name_bed_blast_alignments = data_bed_blast_alignments["name"]
        self.priority = data_bed_blast_alignments["order_index"]
        self.track_color = data_bed_blast_alignments["track_color"]
        # TODO: Think about how to avoid repetition of the group_name everywhere
        self.group_name = data_bed_blast_alignments["group_name"]
        self.database = data_bed_blast_alignments["database"]
        if data_bed_blast_alignments["long_label"]:
            self.long_label = data_bed_blast_alignments["long_label"]
        else:
            self.long_label = self.name_bed_blast_alignments
        #sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")

        # Sort processing
        #subtools.sort(self.input_bigpsl_false_path, sortedBedFile.name)

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + .bb
        trackName = "".join( ( self.name_bed_blast_alignments, '.bb' ) )

        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)

        auto_sql_option = os.path.join(self.tool_directory, 'bigPsl.as')

        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(self.input_bed_blast_alignments_false_path,
                                 self.chromSizesFile.name,
                                 bigBedFile.name,
                                 typeOption='bed12+12',
                                 tab='True',
                                 autoSql=auto_sql_option,
                                 extraIndex='name')

        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.long_label, track_type='bigBed 12 +', visibility='dense',
                         priority=self.priority,
                         track_file=myBigBedFilePath,
                         track_color=self.track_color,
                         group_name=self.group_name,
                         database=self.database
                         )
    '''
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
                                 typeOption='bed12+12',
                                 tab='True',
                                 autoSql=auto_sql_option,
                                 extraIndex='name'
                                 )
        #print("- Bed Blast alignments %s created" % self.trackName)
        # dataURL = "tracks/%s" % trackName
        #
        # trackDb = TrackDb(
        #     trackName=trackName,
        #     longLabel=self.name_bed_simple_repeats,
        #     shortLabel=self.getShortName( self.name_bed_simple_repeats ),
        #     trackDataURL=dataURL,
        #     trackType='bigBed 4 +',
        #     visibility='dense',
        #     priority=self.priority,
        # )
        #
        # self.track = Track(
        #     trackFile=myBigBedFilePath,
        #     trackDb=trackDb,
        # )

    
        #print("- %s created in %s" % (trackName, myBigBedFilePath))
