#! python

import tempfile
import subprocess


def twoBitFileCreator(fastaFile):
    """
    2bit file creator from a fasta file.
    Need faTwoBit kentUtil.
    Output a .2bit file
    """
    twoBitFile = tempfile.NamedTemporaryFile(suffix=".2bit")

    p = subprocess.Popen(
        ['tools/faToTwoBit',
            fastaFile.name,
            twoBitFile.name])

    p.wait()

    return twoBitFile
