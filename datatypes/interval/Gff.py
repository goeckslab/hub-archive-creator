#!/usr/bin/python

import os
import tempfile
import abc

# Internal dependencies
from Interval import Interval
from datatypes.validators.DataValidation import DataValidation
from datatypes.converters.DataConversion import DataConversion

class Gff(Interval):
    def __init__(self):
        super(Gff, self).__init__()
        self.trackType = "bigGenePred"
        self.autoSql = os.path.join(self.tool_directory, 'bigGenePred.as')

    def initSettings(self):
        super(Gff, self).initSettings() 
        self.trackName = "".join( ( self.trackName, ".bb") )
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if "track_color" in self.trackSettings:
            self.extraSettings["color"] = self.trackSettings["track_color"]
        if "group_name" in self.trackSettings:
            self.extraSettings["group"] = self.trackSettings["group_name"]
        self.extraSettings["visibility"] = "dense"
        self.extraSettings["priority"] = self.trackSettings["order_index"]
    
    def createTrack(self):
        self.convertType = self.getConvertType()
        self.options = self.getConvertOptions(typeOption="bed12+8", tab="True", autoSql=self.autoSql)
        self.converter = DataConversion(self.inputFile, self.trackDataURL, self.chromSizesFile.name, self.convertType, self.options)
        self.converter.convertFormats()
    

    @abc.abstractmethod
    def getConvertType(self):
        """return tuple: (dataType, trackType)"""
        return (self.dataType.lower(), self.trackType.lower())


    def getConvertOptions(self, typeOption=None, tab=None, autoSql=None, extraIndex=None):
        options = dict()
        if typeOption:
            options["typeOption"] = typeOption
        if tab:
            options["tab"] = tab
        if autoSql:
            options["autoSql"] = autoSql
        if extraIndex:
            options["extraIndex"] = extraIndex
        return options