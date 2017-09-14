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
from datatypes.interval.cytoBand import cytoBand
from datatypes.interval.BedBlatAlignments import BedBlatAlignments
from datatypes.interval.BedBlastAlignments import BedBlastAlignments
from datatypes.interval.Gff3 import Gff3
from datatypes.interval.Gtf import Gtf
from datatypes.interval.Psl import Psl
from datatypes.sequence.Fasta import Fasta
from util import logger_settings
from util import santitizer

class Reader(object):
    
    def __init__(self, input_json_file):
        self.inputFile = input_json_file
        self.args = self.loadJson()
        self.reader_log = logging.getLogger(__name__)
    
    def loadJson(self):
        #with open(self.inputFile, 'r') as data_file:  
        data_file = codecs.open(self.inputFile, 'r', 'utf-8')  
        args = json.load(data_file)
        return args

    def getOutputDir(self):
        try:
            return self.args["output"]
        except KeyError:
            #print ("output directory is not defined in the input file!")
            self.reader_log.error("output directory is not defined in the input file!")

    def getToolDir(self):
        try:
            return self.args["tool_directory"]
        except KeyError:
            #print ("tool_directory is not defined in the input file!")
            self.reader_log.error("tool_directory is not defined in the input file!")
    
    def getExtFilesPath(self):
        try:
            return self.args["extra_files_path"]
        except KeyError:
            #print ("extra_files_path is not defined in the input file!")
            self.reader_log.error("extra_files_path is not defined in the input file!")

    def getUserEmail(self):
        try:
            return self.args["user_email"]
        except KeyError:
            #print ("user_email is not defined in the input file!")
            self.reader_log.error("user_email is not defined in the input file!")
    
    def getDebugMode(self):
        try:
            return self.args["debug_mode"]
        except KeyError:
            #print ("debug_mode is not defined in the input file!")
            self.reader_log.error("debug_mode is not defined in the input file!")
        
        
    def getRefGenome(self):
        array_inputs_reference_genome = self.args["fasta"]
        # TODO: Replace these with the object Fasta
        input_fasta_file = array_inputs_reference_genome["false_path"]
        input_fasta_file_name = santitizer.sanitize_name_input(array_inputs_reference_genome["name"])
        genome_name = santitizer.sanitize_name_input(self.args["genome_name"])

        self.reader_log.debug("input_fasta_file: " + input_fasta_file)
        self.reader_log.debug("input_fasta_file_name: " + input_fasta_file_name)
        self.reader_log.debug("genome_name: " + genome_name)
        reference_genome = Fasta(input_fasta_file,
                             input_fasta_file_name, genome_name)
        return reference_genome

    def getTracksData(self):
        array_inputs_bam = self.args.get("bam")
        array_inputs_bed_generic = self.args.get("bed")
        array_inputs_bed_cytoBand = self.args.get("cytoBand")
        array_inputs_bed_simple_repeats = self.args.get("bedSimpleRepeats")
        array_inputs_bed_splice_junctions = self.args.get("bedSpliceJunctions")
        array_inputs_bigwig = self.args.get("bigwig")
        array_inputs_gff3 = self.args.get("gff3")
        array_inputs_gtf = self.args.get("gtf")
        array_inputs_psl = self.args.get("psl")
        array_inputs_bed_blat_alignments = self.args.get("bedBlatAlignments")
        array_inputs_bed_blast_alignments = self.args.get("bedBlastAlignments")
        array_inputs_bigbed = self.args.get("bigbed")

        all_datatype_dictionary = dict()
        for (inputs, datatype_class) in [
            (array_inputs_bam, Bam),
            (array_inputs_bed_generic, Bed),
            (array_inputs_bed_cytoBand, cytoBand),
            (array_inputs_bigwig, BigWig),
            (array_inputs_bed_simple_repeats, BedSimpleRepeats),
            (array_inputs_bed_splice_junctions, BedSpliceJunctions),
            (array_inputs_gff3, Gff3),
            (array_inputs_gtf, Gtf),
            (array_inputs_psl, Psl),
            (array_inputs_bed_blat_alignments, BedBlatAlignments),
            (array_inputs_bed_blast_alignments, BedBlastAlignments),
            (array_inputs_bigbed, BigBed)]:
            if inputs:
                all_datatype_dictionary.update(self.create_ordered_datatype_objects(datatype_class, inputs))
        print all_datatype_dictionary
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
            self.reader_log.debug("false_path: " + input_data["false_path"])
            self.reader_log.debug("input_data: " + str(input_data))
            extensionObject = ExtensionClass(input_false_path, input_data)
            extensionObject.generateCustomTrack()
            datatype_dictionary.update({input_data["order_index"]: extensionObject})
        return datatype_dictionary

    def _encodeData(self, data):
        return data.encode('utf-8')
        


