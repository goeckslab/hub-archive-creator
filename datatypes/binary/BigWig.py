#!/usr/bin/python

import os
import shutil
from subprocess import Popen, PIPE
import re

# Internal dependencies
from Binary import Binary
from datatypes.validators.DataValidation import DataValidation



class BigWig(Binary):
    def __init__(self, input_bigwig_path, data_bigwig):
        super(BigWig, self).__init__()
        self.inputFile = input_bigwig_path
        self.trackSettings = data_bigwig
        self.dataType = "bigWig"

    def initSettings(self):
        super(BigWig, self).initSettings()
        self.trackName = "".join( ( self.trackName, ".bigwig" ) )
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        self.trackType=self._determine_track_type(self.inputFile)
        if "track_color" in self.trackSettings:
            self.extraSettings["color"] = self.trackSettings["track_color"]
        if "group_name" in self.trackSettings:
            self.extraSettings["group"] = self.trackSettings["group_name"]
        self.extraSettings["visibility"] = "dense"
        self.extraSettings["priority"] = self.trackSettings["order_index"]
        self.extraSettings["autoScale"] = "on"
        self.extraSettings["maxHeightPixels"] = "100:32:8"
        self.extraSettings["windowingFunction"] = "mean+whiskers"

    def validateData(self):
        self.validator = DataValidation(self.inputFile, self.dataType, self.chromSizesFile.name)
        self.validator.validate()

    def _determine_track_type(self, bw_file):
        """
        bigWig tracks must declare the expected signal range for the data
        (See https://genome.ucsc.edu/goldenpath/help/trackDb/trackDbHub.html).
        This method determines the range of values for a bigWig file using
        the bigWigInfo program.

        Implementation of reading from stdout is based on a Stackoverflow post:
        http://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate

        :param bw_file: path to a bigWig file

        :returns: the bigWig track type
        """
        cmd_ph = Popen(["bigWigInfo", "-minMax", bw_file],
                       stdout=PIPE, bufsize=1)

        with cmd_ph.stdout:
            for line in iter(cmd_ph.stdout.readline, b''):
                bw_type = "bigWig %s" % line.rstrip()

        cmd_ph.wait()

        return bw_type


