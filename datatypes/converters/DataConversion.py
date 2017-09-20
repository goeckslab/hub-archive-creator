#!/usr/bin/python
# -*- coding: utf8 -*-

"""
This class handles the subprocess calls of the different tools used
in HubArchiveCreator
"""

import logging
import os
import subprocess
import sys
import string
import tempfile

from util import subtools

class DataConversion(object):
    
    CONVERT_OPERATIONS = {("bed", "bigbed"): "bedtobigbed",
                          ("bed", "bigpsl"): "bedtobigbed",
                          ("psl", "bigpsl"): "psltobigbed",
                           ("fasta", "twobit"): "fatotwobit",
                           ("gtf", "biggenepred"): "gtftobiggenepred",
                           ("gff3", "biggenepred"): "gff3tobiggenepred"
                           }
    

    def __init__(self, inputFile, outputFile, chromSizesFile, operateType, options=None):
        self.chromSizesFile = chromSizesFile
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.operateType = operateType
        self.options = options
        if not self.operateType or not self.inputFile:
            raise TypeError("the operateType or the input file is not specified!\n")

    def convertFormats(self):
        convertMethod = self.CONVERT_OPERATIONS[self.operateType]
        if convertMethod == "bedtobigbed":
            sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
            subtools.sort(self.inputFile, sortedBedFile.name)
            subtools.bedToBigBed(sortedBedFile.name, self.chromSizesFile, self.outputFile, self.options)

        elif convertMethod == "psltobigbed":
            unsorted_bed_formatted_psl_file = tempfile.NamedTemporaryFile(suffix='.psl')
            sorted_bed_formatted_psl_file = tempfile.NamedTemporaryFile(suffix='psl')
            subtools.pslToBigPsl(self.inputFile, unsorted_bed_formatted_psl_file.name)
            subtools.sort(unsorted_bed_formatted_psl_file.name, sorted_bed_formatted_psl_file.name)
            subtools.bedToBigBed(sorted_bed_formatted_psl_file.name, self.chromSizesFile, self.outputFile, self.options)   

        elif convertMethod == "fatotwobit":
            subtools.faToTwoBit(self.inputFile, self.outputFile)

        elif convertMethod == "gtftobiggenepred":
            unsorted_genePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
            unsorted_bigGenePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsorted.bigGenePred")
            sorted_bigGenePred_file = tempfile.NamedTemporaryFile(suffix=".sorted.bigGenePred")
            subtools.gtfToGenePred(self.inputFile, unsorted_genePred_file.name)
            subtools.genePredToBigGenePred(unsorted_genePred_file.name, unsorted_bigGenePred_file.name)
            subtools.sort(unsorted_bigGenePred_file.name, sorted_bigGenePred_file.name)
            subtools.bedToBigBed(sorted_bigGenePred_file.name, self.chromSizesFile, self.outputFile, self.options)

        elif convertMethod == "gff3tobiggenepred":
            unsorted_genePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
            unsorted_bigGenePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsorted.bigGenePred")
            sorted_bigGenePred_file = tempfile.NamedTemporaryFile(suffix=".sorted.bigGenePred")
            subtools.gff3ToGenePred(self.inputFile, unsorted_genePred_file.name)   
            subtools.genePredToBigGenePred(unsorted_genePred_file.name, unsorted_bigGenePred_file.name)
            subtools.sort(unsorted_bigGenePred_file.name, sorted_bigGenePred_file.name)
            subtools.bedToBigBed(sorted_bigGenePred_file.name, self.chromSizesFile, self.outputFile, self.options)   
        
        else:
            raise Exception("the operation is not defined!\n")

