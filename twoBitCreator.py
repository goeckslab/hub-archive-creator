#! python

import tempfile
import subprocess


def twoBitFileCreator(fastaFile):
    """
    2bit file creator from a fasta file.
    Need faTwoBit kentUtil.
    Output a .2bit file
    """
    twoBitFile = tempfile.NamedTemporaryFile()

    p = subprocess.Popen(
        ['tools/faToTwoBit',
            fastaFile.name,
            twoBitFile.name],
        shell=True)

    p.wait()

    return twoBitFile
