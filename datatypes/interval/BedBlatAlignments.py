#!/usr/bin/python

import os
import tempfile
import string

from BigPsl import BigPsl
from util import subtools


class BedBlatAlignments( BigPsl ):
    def __init__(self, input_bed_blast_alignments_false_path, data_bed_blast_alignments):

        super(BedBlatAlignments, self).__init__(input_bed_blast_alignments_false_path, data_bed_blast_alignments)
        self.seqType = 1
    
    