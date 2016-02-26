#!/usr/bin/python

import os
import tempfile
import subprocess


def twoBitFileCreator(fastaFile, toolDirectory, mySpecieFolder):
    """
    2bit file creator from a fasta file.
    Need faTwoBit kentUtil.
    Output a .2bit file
    """
    baseNameFasta = os.path.basename(fastaFile.name)
    suffixTwoBit, extensionTwoBit = os.path.splitext(baseNameFasta)
    nameTwoBit = suffixTwoBit + '.2bit'

    with open(os.path.join(mySpecieFolder, nameTwoBit), 'w') as twoBitFile:
        p = subprocess.Popen(
            [os.path.join(toolDirectory, 'tools/faToTwoBit'),
                fastaFile.name,
                twoBitFile.name])

        p.wait()

    return twoBitFile
