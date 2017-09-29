#!/usr/bin/python

import os
import shutil
from subprocess import Popen, PIPE
import re

# Internal dependencies
from Binary import Binary
from datatypes.validators.DataValidation import DataValidation
from util.index.DatabaseIndex import DatabaseIndex
from util.index.TrixIndex import TrixIndex


class BigBed(Binary):
    def __init__(self, input_bigbed_path, data_bigbed):
        super(BigBed, self).__init__()
        self.inputFile = input_bigbed_path
        self.trackSettings = data_bigbed
        self.trackType = self._determine_track_type(self.inputFile)
        self.dataType = self.trackType.replace(' ', '')
        self.seqType = None

    def initSettings(self):
        super(BigBed, self).initSettings()
        self.trackName = "".join( ( self.trackName, ".bigbed" ) )
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if "track_color" in self.trackSettings:
            self.extraSettings["color"] = self.trackSettings["track_color"]
        if "group_name" in self.trackSettings:
            self.extraSettings["group"] = self.trackSettings["group_name"]
        self.extraSettings["visibility"] = "dense"
        self.extraSettings["priority"] = self.trackSettings["order_index"]
        if "database" in self.trackSettings:
            self.database_settings = DatabaseIndex(database=self.trackSettings["database"], seqType=self.seqType).setExtLink()
            self.extraSettings.update(self.database_settings)
        if "indexIx" in self.trackSettings and "indexIxx" in self.trackSettings:
            trix_id = self.trackSettings["trix_id"]
            self.trix_settings = TrixIndex(indexIx=self.trackSettings["indexIx"], indexIxx=self.trackSettings["indexIxx"], trackName=self.trackName, mySpecieFolderPath=self.mySpecieFolderPath, trixId=trix_id).setExtLink()
            self.extraSettings.update(self.trix_settings)
    
    def validateData(self):
        self.validator = DataValidation(self.inputFile, self.dataType, self.chromSizesFile.name)
        self.validator.validate()
        

    def getValidateType(self):
        return self._determine_track_type(self.inputFile)

    def _determine_track_type(self, bb_file):
        """
        Determine the number of standard and extra fields using bigBedSummary

        Implementation of reading from stdout is based on a Stackoverflow post:
        http://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate

        :param bb_file: path to a bigBed file

        :returns: the bigBed track type
        """

        cmd_ph = Popen(["bigBedSummary", "-fields", bb_file, "stdout"],
                       stdout=PIPE, bufsize=1)

        pattern = r"(\d+) bed definition fields, (\d+) total fields"

        with cmd_ph.stdout:
            for line in iter(cmd_ph.stdout.readline, b''):
                match = re.match(pattern, line)

                if match:
                    extra_mark = "." if match.group(1) == match.group(2) else "+"
                    bed_type = "bigBed %s %s" % (match.group(1), extra_mark)
                    break

        cmd_ph.wait()

        return bed_type
