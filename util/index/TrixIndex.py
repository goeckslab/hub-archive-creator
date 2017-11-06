#!/usr/bin/python

import os
import collections
import shutil
import logging
from ExternIndex import ExternIndex

class TrixIndex(ExternIndex):
    def __init__(self, indexIx, indexIxx, trackName, mySpecieFolderPath, trixId, **args):
        self.logger = logging.getLogger(__name__)
        self.indexIx = indexIx
        self.indexIxx = indexIxx
        self.trackName = trackName
        self.mySpecieFolderPath = mySpecieFolderPath
        self.index_settings = collections.OrderedDict()
        self.trixId = trixId.rstrip()
        

    def setExtLink(self):
        self.setSearchIndex()
        self.moveIndexFile()
        self.index_settings["searchTrix"] = "trix/%s" % self.indexIxName
        return self.index_settings

    def moveIndexFile(self):
        indexFolder = os.path.join(self.mySpecieFolderPath, 'trix')
        self.indexIxName = "".join( ( self.trackName, ".ix") )
        self.indexIxxName = "".join( ( self.trackName, ".ixx") )
        if not os.path.exists(indexFolder):
            os.makedirs(indexFolder)
        
        # Move index files to the index folder
        self.indexIxPath = os.path.join(indexFolder, self.indexIxName)
        shutil.copyfile(self.indexIx, self.indexIxPath)
        self.indexIxxPath = os.path.join(indexFolder, self.indexIxxName)
        shutil.copyfile(self.indexIxx, self.indexIxxPath)

    def setSearchIndex(self):
        if not self.trixId:
            self.logger.error("Didn't specify Trix Id")
        self.logger.debug("trixId= %s, searchIndex= %s", self.trixId, self.trixId)
        self.index_settings["searchIndex"] = self.trixId
    
        
