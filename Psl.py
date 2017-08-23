import logging
import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from util import subtools


class Psl(Datatype):
    def __init__(self, input_psl_path, data_psl):
        super(Psl, self).__init__()
        self.inputPsl = input_psl_path
        self.pslMetaData = data_psl
        self.trackType = "bigPsl"
        self.bedType = "bed12+12"
    
    def generateCustomTrack(self):
        self.initPslSettings()
        self.convertPslTobigBed()
        # Create the Track Object
        self.createTrack(trackName=self.trackName,
                         longLabel=self.longLabel, 
                         shortLabel=self.shortLabel,
                         trackDataURL=self.trackDataURL,
                         trackType=self.trackType,
                         extra_settings = self.extra_settings
        )
        print("- BigPsl %s created" % self.trackName)  

    def initPslSettings(self):
        self.initRequiredSettings(self.pslMetaData, trackType = self.trackType) 
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        self.trackName = "".join( ( self.trackName, ".bb") )
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if "track_color" in self.pslMetaData:
            self.extra_settings["track_color"] = self.pslMetaData["track_color"]
        if "group_name" in self.pslMetaData:
            self.extra_settings["group_name"] = self.pslMetaData["group_name"]
        self.extra_settings["visibility"] = "dense"
        self.extra_settings["priority"] = self.pslMetaData["order_index"]
    
    def convertPslTobigBed(self):
         # Temporary files
        unsorted_bed_formatted_psl_file = tempfile.NamedTemporaryFile(suffix='.psl')
        sorted_bed_formatted_psl_file = tempfile.NamedTemporaryFile(suffix='psl')

        # Get the bed12+12 with pslToBigPsl
        subtools.pslToBigPsl(self.inputPsl, unsorted_bed_formatted_psl_file.name)

        # Sort the formatted psl into sorted_bed_formatted_psl_file
        subtools.sort(unsorted_bed_formatted_psl_file.name, sorted_bed_formatted_psl_file.name)

        auto_sql_option = os.path.join(self.tool_directory, 'bigPsl.as')
        # bedToBigBed processing
        with open(self.trackDataURL, 'w') as big_psl_file:
            subtools.bedToBigBed(sorted_bed_formatted_psl_file.name,
                                 self.chromSizesFile.name,
                                 big_psl_file.name,
                                 autoSql=auto_sql_option,
                                 typeOption=self.bedType,
                                 tab=True,
                                 extraIndex='name')