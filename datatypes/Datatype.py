#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Super Class of the managed datatype
"""

import os
import tempfile
import collections
import util
import logging
import abc
from abc import ABCMeta
from TrackDb import TrackDb
from datatypes.validators.DataValidation import DataValidation


class Datatype(object):
    __metaclass__ = ABCMeta

    twoBitFile = None
    chromSizesFile = None
    input_fasta_file = None
    extra_files_path = None
    tool_directory = None

    mySpecieFolderPath = None
    myTrackFolderPath = None
 

    def __init__(self):
        not_init_message = "The {0} is not initialized." \
                           "Did you use pre_init static method first?"
        if Datatype.input_fasta_file is None:
            raise TypeError(not_init_message.format('reference genome'))
        if Datatype.extra_files_path is None:
            raise TypeError(not_init_message.format('track Hub path'))
        if Datatype.tool_directory is None:
            raise TypeError(not_init_message.format('tool directory'))
        self.inputFile = None
        self.trackType = None
        self.dataType = None
        self.track = None
        self.trackSettings = dict()
        self.extraSettings = collections.OrderedDict()

    @staticmethod
    def pre_init(reference_genome, two_bit_path, chrom_sizes_file,
                 extra_files_path, tool_directory, specie_folder, tracks_folder):
        Datatype.extra_files_path = extra_files_path
        Datatype.tool_directory = tool_directory

        # TODO: All this should be in TrackHub and not in Datatype
        Datatype.mySpecieFolderPath = specie_folder
        Datatype.myTrackFolderPath = tracks_folder

        Datatype.input_fasta_file = reference_genome

        # 2bit file creation from input fasta
        Datatype.twoBitFile = two_bit_path
        Datatype.chromSizesFile = chrom_sizes_file
    
    def generateCustomTrack(self):
        self.validateData()
        self.initSettings()
        #Create the track file
        self.createTrack()
        # Create the TrackDb Object
        self.createTrackDb()
        logging.debug("- %s %s created", self.dataType, self.trackName)  

    
    @abc.abstractmethod 
    def validateData(self):
        """validate the input data with DataValidation"""
    
    def initSettings(self, trackType = None):
        #Initialize required fields: trackName, longLabel, shortLable
        self.trackName = self.trackSettings["name"]
        if self.trackSettings["long_label"]:
            self.longLabel = self.trackSettings["long_label"]
        else:
            self.longLabel = self.trackName
        if not "short_label" in self.trackSettings:
            self.shortLabel = ""
        else:
            self.shortLabel = self.trackSettings["short_label"]
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if trackType:
            self.trackType = trackType

    @abc.abstractmethod
    def createTrack(self):
        """Create the final track file"""

    def createTrackDb(self):
        self.track = TrackDb(self.trackName, self.longLabel, self.shortLabel, self.trackDataURL, self.trackType, self.extraSettings)

    
   

        
    
        
    '''
    def __init__(self):
        not_init_message = "The {0} is not initialized." \
                           "Did you use pre_init static method first?"
        if Datatype.input_fasta_file is None:
            raise TypeError(not_init_message.format('reference genome'))
        if Datatype.extra_files_path is None:
            raise TypeError(not_init_message.format('track Hub path'))
        if Datatype.tool_directory is None:
            raise TypeError(not_init_message.format('tool directory'))
        self.track = None
        self.extra_settings = collections.OrderedDict()
        

    @staticmethod
    def pre_init(reference_genome, two_bit_path, chrom_sizes_file,
                 extra_files_path, tool_directory, specie_folder, tracks_folder):
        Datatype.extra_files_path = extra_files_path
        Datatype.tool_directory = tool_directory

        # TODO: All this should be in TrackHub and not in Datatype
        Datatype.mySpecieFolderPath = specie_folder
        Datatype.myTrackFolderPath = tracks_folder

        Datatype.input_fasta_file = reference_genome

        # 2bit file creation from input fasta
        Datatype.twoBitFile = two_bit_path
        Datatype.chromSizesFile = chrom_sizes_file
 
    @staticmethod
    def get_largest_scaffold_name(self):
        # We can get the biggest scaffold here, with chromSizesFile
        with open(Datatype.chromSizesFile.name, 'r') as chrom_sizes:
            # TODO: Check if exists
            return chrom_sizes.readline().split()[0]
  

    def createTrack(self, trackName, longLabel, shortLabel, trackDataURL, trackType, extra_settings=None):
        self.track = TrackDb(trackName, longLabel, shortLabel, trackDataURL, trackType, extra_settings)

    def initRequiredSettings(self, trackSettings, trackDataURL = None, trackType = None):
        
        #Initialize required fields: trackName, longLabel, shortLable
      
        self.trackSettings = trackSettings
        self.trackName = self.trackSettings["name"]
        #self.priority = self.trackSettings["order_index"]
        #self.track_color = self.trackSettings["track_color"]
        # TODO: Think about how to avoid repetition of the group_name everywhere
        #self.group_name = self.trackSettings["group_name"]
        #self.database = self.trackSettings["database"]
        if self.trackSettings["long_label"]:
            self.longLabel = self.trackSettings["long_label"]
        else:
            self.longLabel = self.trackName
        if not "short_label" in self.trackSettings:
            self.shortLabel = ""
        else:
            self.shortLabel = self.trackSettings["short_label"]
        self.trackDataURL = trackDataURL
        self.trackType = trackType
    
    def setExtLink(self, database, inputFile, seqType=None, useIframe=True, iframeHeight=None, iframeWidth=None):
        if "NCBI" in database:
            if not seqType:
                self.seqType = int(self.getSeqType(inputFile))
            else:
                self.seqType = seqType
            if self.seqType < 0:
                print self.seqType
                raise Exception("Sequence Type is not set for bigPsl. Stopping the application")
            if self.seqType == 2:
                self.extra_settings["url"] = "https://www.ncbi.nlm.nih.gov/protein/$$"
            elif self.seqType == 1:
                self.extra_settings["url"] = "https://www.ncbi.nlm.nih.gov/nuccore/$$"
            else:
                raise Exception("Sequence Type {0} is not valid for bigPsl. Stopping the application".format(self.seqType))
        elif "UniProt" in database:
            self.extra_settings["url"] = "http://www.uniprot.org/uniprot/$$"
        elif "FlyBase" in database:
            self.extra_settings["url"] = "http://flybase.org/reports/$$"
        else:
            self.extra_settings["url"] = "https://www.ncbi.nlm.nih.gov/gquery/?term=$$"
        self.extra_settings["urlLabel"] = database + " Details:"
        if useIframe:
            self.extra_settings["iframeUrl"] = self.extra_settings["url"]
            if not iframeHeight:
                iframeHeight = "600"
            if not iframeWidth:
                iframeWidth = "800"
            self.extra_settings["iframeOptions"] = "height= %s width= %s" % (iframeHeight, iframeWidth)

    def getSeqType(self, inputFile):
        with open(inputFile, "r") as bigpsl:
            sampleSeq = bigpsl.readline().split()
        if len(sampleSeq) == 25:
            return sampleSeq[-1]
        else:
            return "-1"        
    '''