#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Super Class of the managed datatype
"""

import os
import tempfile
import collections
import shutil
import util
from TrackDb import TrackDb
from datatypes.Datatype import Datatype


class Binary(Datatype):

    def __init__(self):
        super(Binary, self).__init__()

    
    def createTrack(self):
        shutil.copy(self.inputFile, self.trackDataURL)




    
        
     