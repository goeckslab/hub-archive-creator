#!/usr/bin/python

import os
import tempfile

from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class BedSimpleRepeats( Datatype ):
    def __init__(self, input_bed_simple_repeats_false_path, data_bed_simple_repeats):

        super(BedSimpleRepeats, self).__init__()

        self.input_bed_simple_repeats_false_path = input_bed_simple_repeats_false_path
        self.name_bed_simple_repeats = data_bed_simple_repeats["name"]
        self.priority = data_bed_simple_repeats["order_index"]

        sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")

        # Sort processing
        subtools.sort(self.input_bed_simple_repeats_false_path, sortedBedFile.name)

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + .bb
        trackName = "".join( ( self.name_bed_simple_repeats, '.bb' ) )
        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)
        auto_sql_option = "%s%s" % ('-as=', os.path.join(self.tool_directory, 'trf_simpleRepeat.as'))
        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sortedBedFile.name, self.chromSizesFile.name, bigBedFile.name,
                                 typeOption='-type=bed4+12',
                                 autoSql=auto_sql_option)

        # Create the Track Object
        dataURL = "tracks/%s" % trackName

        trackDb = TrackDb(
            trackName=trackName,
            longLabel=self.name_bed_simple_repeats,
            shortLabel=self.getShortName( self.name_bed_simple_repeats ),
            trackDataURL=dataURL,
            trackType='bigBed 4 +',
            visibility='dense',
            priority=self.priority,
        )

        self.track = Track(
            trackFile=myBigBedFilePath,
            trackDb=trackDb,
        )

        print("- %s created in %s" % (trackName, myBigBedFilePath))
