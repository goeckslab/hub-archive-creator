#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Gff import Gff
from datatypes.validators.GtfValidation import GtfValidation


class Gtf(Gff):
    def __init__( self, input_gtf_false_path, data_gtf):

        super(Gtf, self).__init__()
        self.inputFile = input_gtf_false_path
        self.trackSettings = data_gtf
        self.dataType = "gtf"

    def getConvertType(self):
        return (self.dataType.lower(), self.trackType.lower())

    def validateData(self):
        self.validator = GtfValidation(self.inputFile, self.dataType, self.chromSizesFile.name)
        self.inputFile = self.validator.validate()

