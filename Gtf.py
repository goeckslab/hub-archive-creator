#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from util import subtools

'''
class InfoModifiedGtf():
    def __init__(self, is_modified=False, array_modified_lines=[]):
        self.is_modified = is_modified
        self.array_modified_lines = array_modified_lines

    def get_str_modified_lines(self):
        return ','.join(map(str, self.array_modified_lines))
'''

class Gtf( Datatype ):
    def __init__( self, input_gtf_false_path, data_gtf):

        super(Gtf, self).__init__()
        self.inputGTF = input_gtf_false_path
        self.GTFMetaData = data_gtf
        self.trackType = "bigGenePred"
        self.bedType = "bed12+8"

    def generateCustomTrack(self):
        self.initGTFSettings()
        self.convertGTFTobigBed()
        # Create the Track Object
        self.createTrack(trackName=self.trackName,
                         longLabel=self.longLabel, 
                         shortLabel=self.shortLabel,
                         trackDataURL=self.trackDataURL,
                         trackType=self.trackType,
                         extra_settings = self.extra_settings
        )
        # TODO: Use Logging instead of print
        if self.is_modified:
            print("- Warning: Gtf %s created with a modified version of your Gtf because of start/end coordinates issues."
                  % self.trackName)
            print("Here are the lines removed: " + self.get_str_modified_lines())
        else:
            print("- Gtf %s created" % self.trackName)
    
    def initGTFSettings(self):
        self.initRequiredSettings(self.GTFMetaData, trackType = self.trackType) 
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        self.trackName = "".join( ( self.trackName, ".bb") )
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if "track_color" in self.GTFMetaData:
            self.extra_settings["track_color"] = self.GTFMetaData["track_color"]
        if "group_name" in self.GTFMetaData:
            self.extra_settings["group_name"] = self.GTFMetaData["group_name"]
        self.extra_settings["visibility"] = "dense"
        self.extra_settings["priority"] = self.GTFMetaData["order_index"]
        
    def convertGTFTobigBed(self):
        # TODO: See if we need these temporary files as part of the generated files
        genePredFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
        unsorted_bigGenePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsorted.bigGenePred")
        sorted_bigGenePred_file = tempfile.NamedTemporaryFile(suffix=".sortedBed.bigGenePred")
        # GtfToGenePred
        ## Checking the integrity of the inputs
        modified_gtf = self._checkAndFixGtf()
        ## Processing the gtf
        subtools.gtfToGenePred(self.inputGTF, genePredFile.name)
        # genePredToBigGenePred processing
        subtools.genePredToBigGenePred(genePredFile.name, unsorted_bigGenePred_file.name)
        # Sort processing
        subtools.sort(unsorted_bigGenePred_file.name, sorted_bigGenePred_file.name)
        # bedToBigBed processing
        auto_sql_option = os.path.join(self.tool_directory, 'bigGenePred.as')
        with open(self.trackDataURL, 'w') as self.bigBedFile:
            subtools.bedToBigBed(sorted_bigGenePred_file.name,
                                 self.chromSizesFile.name,
                                 self.bigBedFile.name,
                                 autoSql=auto_sql_option,
                                 typeOption=self.bedType,
                                 tab=True,
                                 extraIndex='name')

    def _checkAndFixGtf(self):
        """
        Call _checkAndFixGtf, check the integrity of gtf file, 
        if coordinates exceed chromosome size, either removed the whole line(s) or truncated to the end of the scaffold 
        depending on the user choice
        default: remove the whole line(s)
        """
        # Set the boolean telling if we had to modify the file
        self.is_modified = False
        self.array_modified_lines = []
        # Create a temp gtf just in case we have issues
        temp_gtf = tempfile.NamedTemporaryFile(bufsize=0, suffix=".gtf", delete=False)

        # TODO: Get the user choice and use it
        # TODO: Check if the start > 0 and the end <= chromosome size
        # Get the chrom.sizes into a dictionary to have a faster access
        # TODO: Think about doing this in Datatype.py, so everywhere we have access to this read-only dictionary
        dict_chrom_sizes = {}
        with open(self.chromSizesFile.name, 'r') as chromSizes:
            lines = chromSizes.readlines()
            for line in lines:
                fields = line.split()
                # fields[1] should be the name of the scaffold
                # fields[2] should be the size of the scaffold
                # TODO: Ensure this is true for all lines
                dict_chrom_sizes[fields[0]] = fields[1]

        # Parse the GTF and check each line using the chrom sizes dictionary
        with open(temp_gtf.name, 'a+') as tmp:
            with open(self.inputGTF, 'r') as gtf:
                lines = gtf.readlines()
                for index, line in enumerate(lines):
                    # If this is not a comment, we check the fields
                    if not line.startswith('#'):
                        fields = line.split()
                        # We are interested in fields[0] => Seqname (scaffold)
                        # We are interested in fields[3] => Start of the scaffold
                        # We are interested in fields[4] => End of the scaffold
                        scaffold_size = dict_chrom_sizes[fields[0]]
                        start_position = fields[3]
                        end_position = fields[4]

                        if start_position > 0 and end_position <= scaffold_size:
                            # We are good, so we copy this line
                            tmp.write(line)
                            tmp.write(os.linesep)


                        # The sequence is not good, we are going to process it regarding the user choice
                        # TODO: Process the user choice
                        # By default, we are assuming the user choice is to remove the lines: We don't copy it

                        # If we are here, it means the gtf has been modified
                        else:
                            # We save the line for the feedback to the user
                            self.array_modified_lines.append(index + 1)

                            if self.is_modified is False:
                                self.is_modified = True
                            else:
                                pass
                    else:
                        tmp.write(line)
                        tmp.write(os.linesep)

        # Once the process it completed, we just replace the path of the gtf
        self.inputGTF = temp_gtf.name

        # TODO: Manage the issue with the fact the dataset is going to still exist on the disk because of delete=False
        #return modified_gtf
    
    def get_str_modified_lines(self):
        return ','.join(map(str, self.array_modified_lines))