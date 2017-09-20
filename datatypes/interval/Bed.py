#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Interval import Interval
from datatypes.validators.DataValidation import DataValidation
from datatypes.converters.DataConversion import DataConversion

class Bed(Interval):
    def __init__(self, inputBedGeneric, data_bed_generic):
        super(Bed, self).__init__()
        self.inputFile = inputBedGeneric
        self.trackSettings = data_bed_generic
        self.trackType = "bigBed"
        self.dataType = "bed"
        self.bedFields = None
        self.extFields = None

    def initSettings(self):
        super(Bed, self).initSettings(trackType = self.trackType) 
        self.trackName = "".join( ( self.trackName, ".bb") )
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if "track_color" in self.trackSettings:
            self.extraSettings["color"] = self.trackSettings["track_color"]
        if "group_name" in self.trackSettings:
            self.extraSettings["group"] = self.trackSettings["group_name"]
        self.extraSettings["visibility"] = "dense"
        self.extraSettings["priority"] = self.trackSettings["order_index"]

    def createTrack(self):
        #self.sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        #subtools.sort(self.inputFile, self.sortedBedFile.name)
        self.convertType = self.getConvertType()
        self.converter = DataConversion(self.inputFile, self.trackDataURL, self.chromSizesFile.name, self.convertType)
        self.converter.convertFormats()

    def validateData(self):
        self.validator = DataValidation(self.inputFile, self.getValidateType(), self.chromSizesFile.name)
        self.validator.validate()
        
    def getBedFields(self):
        """count number of bed fields for generic bed format"""
        with open(self.inputFile, 'r') as bed:
            l = bed.readline().split()
            return len(l)

    def getValidateType(self):
        if not self.bedFields:
            return self.dataType + str(self.getBedFields())
        elif not self.extFields:
            return self.dataType + str(self.bedFields)
        else:
            return self.dataType + str(self.bedFields) + "+" + str(self.extFields)

