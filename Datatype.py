#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Super Class of the managed datatype
"""

import os

from util import subtools


class Datatype(object):
    def __init__( self, input_fasta_file, extra_files_path, tool_directory ):

        self.input_fasta_file = input_fasta_file
        self.extra_files_path = extra_files_path
        self.tool_directory = tool_directory

        # Construction of the arborescence
        # TODO: Change the hard-coded path with a input based one
        self.mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # TODO: Refactor the name of the folder "tracks" into one variable, and should be inside TrackHub object
        self.myTrackFolderPath = os.path.join(self.mySpecieFolderPath, "tracks")

        # TODO: Redundant, should be refactored because they are all doing it...into hubArchiveCreator?
        # 2bit file creation from input fasta
        self.twoBitFile = subtools.faToTwoBit(self.input_fasta_file, self.mySpecieFolderPath)