#!/usr/bin/python

import os
import tempfile

from Bed import Bed
from TrackDb import TrackDb
from datatypes.validators.DataValidation import DataValidation
from datatypes.converters.DataConversion import DataConversion


class CytoBand( Bed ):
    def __init__(self, input_bed_cytoBand_false_path, data_bed_cytoBand):

        super(CytoBand, self).__init__(input_bed_cytoBand_false_path, data_bed_cytoBand)
        self.bedFields = 4
        self.extFields = 1
        self.autoSql = os.path.join(self.tool_directory, 'cytoBandIdeo.as')

    def validateData(self):
        self.validateOptions = self.getValidateOptions(tab="True", autoSql=self.autoSql)
        self.validator = DataValidation(self.inputFile, self.getValidateType(), self.chromSizesFile.name, self.validateOptions)
        self.validator.validate()
    
    def createTrack(self):
        self.convertType = self.getConvertType()
        self.options = self.getConvertOptions(typeOption=self.getValidateType(), tab="True", autoSql=self.autoSql)
        self.converter = DataConversion(self.inputFile, self.trackDataURL, self.chromSizesFile.name, self.convertType, self.options)
        self.converter.convertFormats()

    def createTrackDb(self):
        self.track = TrackDb('cytoBandIdeo', self.longLabel, self.shortLabel, self.trackDataURL, self.trackType, self.extraSettings)
