#!/usr/bin/python

import os
import shutil
from subprocess import Popen, PIPE
import re

# Internal dependencies
from Datatype import Datatype

class BigBed(Datatype):
    """ Configurations for creating the bigBed evidence track """

    def __init__(self, input_bigbed_path, data_bigbed):
        super(BigBed, self).__init__()

        self.track = None

        self.input_bigbed_path = input_bigbed_path
        self.name_bigbed = data_bigbed["name"]
        self.priority = data_bigbed["order_index"]
        self.track_color = data_bigbed["track_color"]
        self.group_name = data_bigbed["group_name"]
        self.database = data_bigbed["database"]

        track_name = "".join((self.name_bigbed, ".bigbed"))
        if data_bigbed["long_label"]:
            self.long_label = data_bigbed["long_label"]
        else:
            self.long_label = self.name_bigbed

        bigbed_file_path = os.path.join(self.myTrackFolderPath, track_name)

        track_type = self.determine_track_type(input_bigbed_path)

        shutil.copy(self.input_bigbed_path, bigbed_file_path)

        # Create the Track Object
        self.createTrack(file_path=track_name,
                         track_name=track_name,
                         long_label=self.long_label,
                         track_type=track_type,
                         visibility='hide',
                         priority=self.priority,
                         track_file=bigbed_file_path,
                         track_color=self.track_color,
                         group_name=self.group_name,
                         database=self.database)

        print "- BigBed %s created" % self.name_bigbed


    def determine_track_type(self, bb_file):
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
