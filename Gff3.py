#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class Gff3( Datatype ):
    def __init__(self, input_Gff3_false_path, data_gff3):
        super( Gff3, self ).__init__()
        self.inputGFF3 = input_Gff3_false_path
        self.GFF3MetaData = data_gff3
        self.trackType = "bigGenePred"
        self.bedType = "bed12+8"

    def generateCustomTrack(self):
        self.initGFF3Settings()
        self.convertGFF3TobigBed()
        # Create the Track Object
        self.createTrack(trackName=self.trackName,
                         longLabel=self.longLabel, 
                         shortLabel=self.shortLabel,
                         trackDataURL=self.trackDataURL,
                         trackType=self.trackType,
                         extra_settings = self.extra_settings
        )
        print("- GFF3 %s created" % self.trackName)  
    
    def initGFF3Settings(self):
        self.initRequiredSettings(self.GFF3MetaData, trackType = self.trackType) 
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        self.trackName = "".join( ( self.trackName, ".bb") )
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if "track_color" in self.GFF3MetaData:
            self.extra_settings["track_color"] = self.GFF3MetaData["track_color"]
        if "group_name" in self.GFF3MetaData:
            self.extra_settings["group_name"] = self.GFF3MetaData["group_name"]
        self.extra_settings["visibility"] = "dense"
        self.extra_settings["priority"] = self.GFF3MetaData["order_index"]
        
    def convertGFF3TobigBed(self):
        # TODO: See if we need these temporary files as part of the generated files
        unsorted_genePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
        unsorted_bigGenePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsorted.bigGenePred")
        sorted_bigGenePred_file = tempfile.NamedTemporaryFile(suffix=".sorted.bigGenePred")

        # gff3ToGenePred processing
        subtools.gff3ToGenePred(self.inputGFF3, unsorted_genePred_file.name)

        # genePredToBigGenePred
        subtools.genePredToBigGenePred(unsorted_genePred_file.name, unsorted_bigGenePred_file.name)

        # Sort processing
        subtools.sort(unsorted_bigGenePred_file.name, sorted_bigGenePred_file.name)

        # TODO: Check if no errors

        # bedToBigBed processing
        auto_sql_option = os.path.join(self.tool_directory, 'bigGenePred.as')
        with open(self.trackDataURL, 'w') as self.bigBedFile:
            subtools.bedToBigBed(sorted_bigGenePred_file.name,
                                 self.chromSizesFile.name,
                                 self.bigBedFile.name,
                                 autoSql=auto_sql_option,
                                 typeOption=self.bedType,
                                 tab=True,
                                 extraIndex='name')
