#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Super Class of the managed datatype
"""

import os

from util import subtools


class Datatype(object):

    twoBitFile = None

    def __init__( self, input_fasta_file, extra_files_path, tool_directory ):

        self.input_fasta_file = input_fasta_file
        self.extra_files_path = extra_files_path
        self.tool_directory = tool_directory

        self.twoBitFile = None

        # Construction of the arborescence
        # TODO: Change the hard-coded path with a input based one
        self.mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # TODO: Refactor the name of the folder "tracks" into one variable, and should be inside TrackHub object
        self.myTrackFolderPath = os.path.join(self.mySpecieFolderPath, "tracks")

        # TODO: Redundant, should be refactored because they are all doing it...into hubArchiveCreator?
        # 2bit file creation from input fasta
        if not Datatype.twoBitFile:
            print "We create the self.twoBit in " + self.__class__.__name__
            Datatype.twoBitFile = subtools.faToTwoBit(self.input_fasta_file, self.mySpecieFolderPath)

        # TODO: Remove this by saying to all children classes to use "Datatype.twoBitFile" instead
        self.twoBitFile = Datatype.twoBitFile

    @staticmethod
    def pre_init(extra_files_path, reference_genome):
        print "Hello!"

    def getShortName( self, name_to_shortify ):
        # Slice to get from Long label the short label
        short_label_slice = slice(0, 15)

        return name_to_shortify[short_label_slice]