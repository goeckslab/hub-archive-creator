#!/usr/bin/python

import os
import tempfile
import string
import logging

from Interval import Interval
from util.index.DatabaseIndex import DatabaseIndex
from util.index.TrixIndex import TrixIndex
from datatypes.validators.DataValidation import DataValidation
from datatypes.converters.DataConversion import DataConversion


class BigPsl(Interval):
    def __init__(self, input_bigpsl_false_path, data_bigpsl):
    
        super(BigPsl, self).__init__()
        self.inputFile = input_bigpsl_false_path
        self.trackSettings = data_bigpsl
        self.trackType = "bigPsl"
        self.dataType = "bed"
        self.bedFields = 12
        self.extFields = 12
        self.seqType = None
        self.autoSql = os.path.join(self.tool_directory, 'bigPsl.as')
        self.logger = logging.getLogger(__name__)
    
    def initSettings(self):
        super(BigPsl, self).initSettings()
        self.trackName = "".join( ( self.trackName, ".bb") )
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if "track_color" in self.trackSettings:
            self.extraSettings["color"] = self.trackSettings["track_color"]
        if "group_name" in self.trackSettings:
            self.extraSettings["group"] = self.trackSettings["group_name"]
        self.extraSettings["visibility"] = "dense"
        self.extraSettings["priority"] = self.trackSettings["order_index"] 
        if self.seqType is None:
            self.seqType = self._getSeqType()
        if "database" in self.trackSettings:
            self.database_settings = DatabaseIndex(database=self.trackSettings["database"], seqType=self.seqType).setExtLink()
            self.extraSettings.update(self.database_settings)
        if "index_ix" in self.trackSettings and "index_ixx" in self.trackSettings:
            self.trix_id = self.extraSettings.get("trix_id")
            if not self.trix_id:
                self.logger.info("Didn't specify the ID for Trix index for BigBed file: %s. \n Will use \"name\" as default", self.trackName)
                self.trix_id = "name"
            self.trix_settings = TrixIndex(indexIx=self.trackSettings["index_ix"], indexIxx=self.trackSettings["index_ixx"], trackName=self.trackName, mySpecieFolderPath=self.mySpecieFolderPath, trixId=self.trix_id).setExtLink()
            self.extraSettings.update(self.trix_settings)
            self.extraIndex = self.trix_id
        else:
            self.extraIndex = "name"
            self.extraSettings["searchIndex"] = "name"
            

    def validateData(self):
        self.validateOptions = self.getValidateOptions(tab="True", autoSql=self.autoSql)
        self.validator = DataValidation(self.inputFile, self.getValidateType(), self.chromSizesFile.name, self.validateOptions)
        self.validator.validate()

    def createTrack(self):
        self.convertType = self.getConvertType()
        self.options = self.getConvertOptions(typeOption=self.getValidateType(), tab="True", autoSql=self.autoSql, extraIndex=self.extraIndex)
        self.converter = DataConversion(self.inputFile, self.trackDataURL, self.chromSizesFile.name, self.convertType, self.options)
        self.converter.convertFormats()
    
    def getValidateType(self):
        if not self.bedFields or not self.extFields:
            raise Exception("Invalid bigPsl format, no {0} or {1}".format("bedFields", "extFields"))
        return self.dataType + str(self.bedFields) + "+" + str(self.extFields)
    
    def _getSeqType(self):
        with open(self.inputFile, "r") as bigpsl:
            sampleSeq = bigpsl.readline().split()
        if len(sampleSeq) == 25:
            return sampleSeq[-1]
        else:
            return None      
