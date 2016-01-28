#! python

import os
import tempfile
import subprocess


def twoBitFileCreator(fastaFile):
    """
    2bit file creator from a fasta file.
    Need faTwoBit kentUtil.
    Output a .2bit file
    """
    baseNameFasta = os.path.basename(fastaFile.name)
    suffixTwoBit, extensionTwoBit = os.path.splitext(baseNameFasta)
    nameTwoBit = suffixTwoBit + '.2bit'

    with open(nameTwoBit, 'w') as twoBitFile:
        p = subprocess.Popen(
            ['tools/faToTwoBit',
                fastaFile.name,
                twoBitFile.name])

        p.wait()

    return twoBitFile
