#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Super Class of the managed datatype
"""

import os
import tempfile
import collections
import shutil
import abc
import util
from TrackDb import TrackDb
from datatypes.Datatype import Datatype


class Interval(Datatype):

    def __init__(self):
        super(Interval, self).__init__()

    def getConvertType(self):
        return (self.dataType.lower(), self.trackType.lower())

    def getValidateOptions(self, tab=None, autoSql=None):
        options = dict()
        if tab:
            options["tab"] = tab
        if autoSql:
            options["autoSql"] = autoSql
        return options

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

    



    