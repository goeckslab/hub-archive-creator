import logging
import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from util import subtools


class Psl(Datatype):
    def __init__(self, input_psl_path, data_psl):
        super(Psl, self).__init__()

        self.track = None

        self.input_psl_path = input_psl_path
        self.name_psl = data_psl["name"]
        self.priority = data_psl["order_index"]
        self.track_color = data_psl["track_color"]
        # TODO: Think about how to avoid repetition of the group_name everywhere
        self.group_name = data_psl["group_name"]
        self.database = data_psl["database"]
        if data_psl["long_label"]:
            self.long_label = data_psl["long_label"]
        else:
            self.long_label = self.name_psl
        # Temporary files
        unsorted_bed_formatted_psl_file = tempfile.NamedTemporaryFile(suffix='.psl')
        sorted_bed_formatted_psl_file = tempfile.NamedTemporaryFile(suffix='psl')

        # Get the bed12+12 with pslToBigPsl
        subtools.pslToBigPsl(input_psl_path, unsorted_bed_formatted_psl_file.name)

        # Sort the formatted psl into sorted_bed_formatted_psl_file
        subtools.sort(unsorted_bed_formatted_psl_file.name, sorted_bed_formatted_psl_file.name)

        # Get the binary indexed bigPsl with bedToBigBed
        trackName = "".join((self.name_psl, ".bb"))

        auto_sql_option = os.path.join(self.tool_directory, 'bigPsl.as')

        my_big_psl_file_path = os.path.join(self.myTrackFolderPath, trackName)

        logging.debug("Hello")

        with open(my_big_psl_file_path, 'w') as big_psl_file:
            subtools.bedToBigBed(sorted_bed_formatted_psl_file.name,
                                 self.chromSizesFile.name,
                                 big_psl_file.name,
                                 autoSql=auto_sql_option,
                                 typeOption='bed12+12',
                                 tab=True,
                                 extraIndex='name')

        # Create the Track Object
        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.long_label,
                         track_type='bigPsl', visibility='dense',
                         priority=self.priority,
                         track_file=my_big_psl_file_path,
                         track_color=self.track_color,
                         group_name=self.group_name,
                         database=self.database)

        print("- BigPsl %s created" % self.name_psl)