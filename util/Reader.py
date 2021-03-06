import os
import json
import logging
import codecs


# Internal dependencies
from datatypes.binary.Bam import Bam
from datatypes.binary.BigWig import BigWig
from datatypes.binary.BigBed import BigBed
from datatypes.interval.Bed import Bed
from datatypes.interval.BedSimpleRepeats import BedSimpleRepeats
from datatypes.interval.BedSpliceJunctions import BedSpliceJunctions
from datatypes.interval.CytoBand import CytoBand
from datatypes.interval.BedBlatAlignments import BedBlatAlignments
from datatypes.interval.BedBlastAlignments import BedBlastAlignments
from datatypes.interval.Gff3 import Gff3
from datatypes.interval.Gtf import Gtf
from datatypes.interval.Psl import Psl
from datatypes.sequence.Fasta import Fasta
from util import santitizer

class Reader(object):
    
    DATATYPE_CLASS = [Bam, BigWig, BigBed, Bed, BedSimpleRepeats, BedSpliceJunctions, CytoBand, BedBlatAlignments, BedBlastAlignments, Gff3, Gtf, Psl, Fasta]

    def __init__(self, input_json_file):
        self.inputFile = input_json_file
        self.args = self.loadJson()
        
    
    def loadJson(self):
        try:
            data_file = codecs.open(self.inputFile, 'r', 'utf-8')   
            return json.load(data_file) 
        except IOError:
            print "Cannot find JSON file\n"
            exit(1)

    def getToolDir(self):
        try:
            return self.args["tool_directory"]
        except KeyError:
            print ("tool_directory is not defined in the input file!")
            exit(1)

    def getExtFilesPath(self):
        try:
            return self.args["extra_files_path"]
        except KeyError:
            print ("extra_files_path is not defined in the input file!")
            exit(1)

    def getUserEmail(self):
        try:
            return self.args["user_email"]
        except KeyError:
            print ("user_email is not defined in the input file!")
            exit(1)
    
    def getDebugMode(self):
        try:
            return self.args["debug_mode"]
        except KeyError:
            print ("debug_mode is not defined in the input file!")
            exit(1)
        
        
    def getRefGenome(self):
        array_inputs_reference_genome = self.args["fasta"]
        # TODO: Replace these with the object Fasta
        input_fasta_file = array_inputs_reference_genome["false_path"]
        input_fasta_file_name = santitizer.sanitize_name_input(array_inputs_reference_genome["name"])
        genome_name = santitizer.sanitize_name_input(self.args["genome_name"])
        reference_genome = Fasta(input_fasta_file,
                             input_fasta_file_name, genome_name)
        return reference_genome
    

    def getTracksData(self):
        self.logger = logging.getLogger(__name__)
        all_datatype_dictionary = dict()
        for datatype in self.DATATYPE_CLASS:
            class_name = datatype.__name__
            array_inputs = self.args.get(str(class_name))
            if array_inputs:
                self.logger.debug("Create %s objects\n", class_name)
                self.logger.debug("array_inputs: %s", array_inputs)
                all_datatype_dictionary.update(self.create_ordered_datatype_objects(datatype, array_inputs))
               
        return all_datatype_dictionary

    def create_ordered_datatype_objects(self, ExtensionClass, array_inputs):
        """
        Function which executes the creation all the necessary files / folders for a special Datatype, for TrackHub
        and update the dictionary of datatype

        :param ExtensionClass:
        :param array_inputs:
        :type ExtensionClass: Datatype
        :type array_inputs: list[string]
        """

        datatype_dictionary = {}

        # TODO: Optimize this double loop
        for input_data in array_inputs:
            input_false_path = input_data["false_path"]
            # if the file is empty, skip the rest
            if os.path.isfile(input_false_path) and os.path.getsize(input_false_path) > 0:
                input_data["name"] = santitizer.sanitize_name_input(input_data["name"])
                extensionObject = ExtensionClass(input_false_path, input_data)
                extensionObject.generateCustomTrack()
                datatype_dictionary.update({input_data["order_index"]: extensionObject})
            else:
                self.logger.info("The input file: %s is empty, skip creating the track for this data", input_data["name"])
        return datatype_dictionary

    
        


