#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from util import subtools

class InfoModifiedGtf():
    def __init__(self, is_modified=False, array_modified_lines=[]):
        self.is_modified = is_modified
        self.array_modified_lines = array_modified_lines

    def get_str_modified_lines(self):
        return ','.join(map(str, self.array_modified_lines))

class Gtf( Datatype ):
    def __init__( self, input_gtf_false_path, data_gtf):

        super(Gtf, self).__init__()

        self.track = None

        self.input_gtf_false_path = input_gtf_false_path
        self.name_gtf = data_gtf["name"]
        self.priority = data_gtf["order_index"]
        self.track_color = data_gtf["track_color"]
        # TODO: Think about how to avoid repetition of the group_name everywhere
        self.group_name = data_gtf["group_name"]

        #print "Creating TrackHub GTF from (falsePath: %s; name: %s)" % ( self.input_gtf_false_path, self.name_gtf)

        # TODO: See if we need these temporary files as part of the generated files
        genePredFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
        unsorted_bigGenePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsorted.bigGenePred")
        sorted_bigGenePred_file = tempfile.NamedTemporaryFile(suffix=".sortedBed.bigGenePred")

        # GtfToGenePred
        ## Checking the integrity of the inputs
        modified_gtf = self._checkAndFixGtf()

        ## Processing the gtf
        subtools.gtfToGenePred(self.input_gtf_false_path, genePredFile.name)

        # TODO: From there, refactor because common use with Gff3.py
        # genePredToBigGenePred processing
        subtools.genePredToBigGenePred(genePredFile.name, unsorted_bigGenePred_file.name)

        # Sort processing
        subtools.sort(unsorted_bigGenePred_file.name, sorted_bigGenePred_file.name)

        # bedToBigBed processing
        trackName = "".join( ( self.name_gtf, ".bb") )

        auto_sql_option = os.path.join(self.tool_directory, 'bigGenePred.as')

        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)

        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sorted_bigGenePred_file.name,
                                 self.chromSizesFile.name,
                                 bigBedFile.name,
                                 autoSql=auto_sql_option,
                                 typeOption='bed12+8',
                                 tab=True)


        # Create the Track Object
        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.name_gtf, track_type='bigGenePred',
                         visibility='dense', priority=self.priority,
                         track_file=myBigBedFilePath,
                         track_color=self.track_color,
                         group_name=self.group_name)

        # TODO: Use Logging instead of print
        if modified_gtf.is_modified:
            print("- Warning: Gtf %s created with a modified version of your Gtf because of start/end coordinates issues."
                  % self.name_gtf)
            print("Here are the lines removed: " + modified_gtf.get_str_modified_lines())
        else:
            print("- Gtf %s created" % self.name_gtf)

    def _checkAndFixGtf(self):
        """
        Call _checkAndFixGtf, check the integrity of gtf file, 
        if coordinates exceed chromosome size, either removed the whole line(s) or truncated to the end of the scaffold 
        depending on the user choice
        default: remove the whole line(s)
        """
        # Set the boolean telling if we had to modify the file
        modified_gtf = InfoModifiedGtf()

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
            with open(self.input_gtf_false_path, 'r') as gtf:
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
                            modified_gtf.array_modified_lines.append(index + 1)

                            if modified_gtf.is_modified is False:
                                modified_gtf.is_modified = True
                            else:
                                pass
                    else:
                        tmp.write(line)
                        tmp.write(os.linesep)

        # Once the process it completed, we just replace the path of the gtf
        self.input_gtf_false_path = temp_gtf.name

        # TODO: Manage the issue with the fact the dataset is going to still exist on the disk because of delete=False

        return modified_gtf
