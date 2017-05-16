#!/usr/bin/python
# -*- coding: utf8 -*-

"""
This class handles the subprocess calls of the different tools used
in HubArchiveCreator
"""

import logging
import os
import subprocess
import sys
import string

class PopenError(Exception):
    def __init__(self, cmd, error, return_code):
        self.cmd = cmd
        self.error = error
        self.return_code = return_code

    def __str__(self):
        message = "The subprocess {0} has returned the error: {1}.".format(self.cmd, self.return_code)
        message = ','.join((message, "Its error message is: {0}".format(self.error)))
        return repr(message)

def _handleExceptionAndCheckCall(array_call, **kwargs):
    """
    This class handle exceptions and call the tool.
    It maps the signature of subprocess.check_call:
    See https://docs.python.org/2/library/subprocess.html#subprocess.check_call
    """
    stdout = kwargs.get('stdout', subprocess.PIPE)
    stderr = kwargs.get('stderr', subprocess.PIPE)
    shell = kwargs.get('shell', False)

    cmd = array_call[0]

    output = None
    error = None

    # TODO: Check the value of array_call and <=[0]
    logging.debug("Calling {0}:".format(cmd))

    logging.debug("---------")

    # TODO: Use universal_newlines option from Popen?
    try:
        p = subprocess.Popen(array_call, stdout=stdout, stderr=stderr, shell=shell)

        # TODO: Change this because of possible memory issues => https://docs.python.org/2/library/subprocess.html#subprocess.Popen.communicate

        output, error = p.communicate()

        if stdout == subprocess.PIPE:
            logging.debug("\t{0}".format(output))
        else:
            logging.debug("\tOutput in file {0}".format(stdout.name))
        # If we detect an error from the subprocess, then we raise an exception
        # TODO: Manage if we raise an exception for everything, or use CRITICAL etc... but not stop process
        # TODO: The responsability of returning a sys.exit() should not be there, but up in the app.
        if p.returncode:
            if stderr == subprocess.PIPE:
                raise PopenError(cmd, error, p.returncode)
            else:
                # TODO: To Handle properly with a design behind, if we received a option as a file for the error
                raise Exception("Error when calling {0}. Error as been logged in your file {1}. Error code: {2}"\
                                .format(cmd, stderr.name, p.returncode))

    except OSError as e:
        message = "The subprocess {0} has encountered an OSError: {1}".format(cmd, e.strerror)
        if e.filename:
            message = '\n'.join((message, ", against this file: {0}".format(e.filename)))
        logging.error(message)
        sys.exit(-1)
    except PopenError as p:
        message = "The subprocess {0} has returned the error: {1}.".format(p.cmd, p.return_code)
        message = '\n'.join((message, "Its error message is: {0}".format(p.error)))

        logging.exception(message)

        sys.exit(p.return_code)
    except Exception as e:
        message = "The subprocess {0} has encountered an unknown error: {1}".format(cmd, e)
        logging.exception(message)

        sys.exit(-1)
    return p

def twoBitInfo(two_bit_file_name, two_bit_info_file):
    """
    Call twoBitInfo and write the result into twoBit_info_file
    :param two_bit_file_name:
    :param two_bit_info_file:
    :return the subprocess.check_call return object:
    """
    array_call = ['twoBitInfo', two_bit_file_name, two_bit_info_file]
    p = _handleExceptionAndCheckCall(array_call)
    return p

def faToTwoBit(fasta_file_name, twoBitFile):
    """
    This function call faToTwoBit UCSC tool, and return the twoBitFile
    :param fasta_file_name:
    :param mySpecieFolder:
    :return:
    """

    array_call = ['faToTwoBit', fasta_file_name, twoBitFile]
    _handleExceptionAndCheckCall(array_call)

    return twoBitFile

def gtfToGenePred(input_gtf_file_name, gene_pred_file_name):
    """
    Call gtfToGenePred and write the result into gene_pred_file_name
    :param input_gtf_file_name:
    :param gene_pred_file_name:
    :return:
    """
    array_call = ['gtfToGenePred', input_gtf_file_name, gene_pred_file_name]
    p = _handleExceptionAndCheckCall(array_call)
    return p

def gff3ToGenePred(input_gff3_file_name, gene_pred_file_name):
    """
    Call gff3ToGenePred and write the result into gene_pred_file_name
    :param input_gff3_file_name:
    :param gene_pred_file_name:
    :return:
    """
    array_call = ['gff3ToGenePred', input_gff3_file_name, gene_pred_file_name]
    p = _handleExceptionAndCheckCall(array_call)
    return p

def genePredToBigGenePred(gene_pred_file_name, unsorted_bigGenePred_file_name):
    """
    Call genePredToBigGenePred and write the result into unsorted_bigGenePred_file_name
    :param gene_pred_file_name:
    :param unsorted_bigGenePred_file_name:
    :return:
    """
    array_call = ['genePredToBigGenePred',
                  gene_pred_file_name,
                  unsorted_bigGenePred_file_name]
    p = _handleExceptionAndCheckCall(array_call)
    return p

def genePredToBed(gene_pred_file_name, unsorted_bed_file_name):
    """
    Call genePredToBed and write the result into unsorted_bed_file_name
    :param gene_pred_file_name:
    :param unsorted_bed_file_name:
    :return:
    """
    array_call = ['genePredToBed', gene_pred_file_name, unsorted_bed_file_name]
    p = _handleExceptionAndCheckCall(array_call)
    return p

def sort(unsorted_bed_file_name, sorted_bed_file_name):
    """
    Call sort with -k1,1 -k2,2n on unsorted_bed_file_name and write the result into sorted_bed_file_name
    :param unsorted_bed_file_name:
    :param sorted_bed_file_name:
    :return:
    """
    array_call = ['sort', '-k', '1,1', '-k', '2,2n', unsorted_bed_file_name, '-o', sorted_bed_file_name]
    p = _handleExceptionAndCheckCall(array_call)
    return p

def sortChromSizes(two_bit_info_file_name, chrom_sizes_file_name):
    """
    Call sort with -k2rn on two_bit_info_file_name and write the result into chrom_sizes_file_name
    :param two_bit_info_file_name:
    :param chrom_sizes_file_name:
    :return:
    """
    array_call = ['sort', '-k2rn', two_bit_info_file_name, '-o', chrom_sizes_file_name]
    p = _handleExceptionAndCheckCall(array_call)
    return p

def bedToBigBed(sorted_bed_file_name, chrom_sizes_file_name, big_bed_file_name,
                typeOption=None, autoSql=None, tab=False):
    """
    Call bedToBigBed on sorted_bed_file_name, using chrom_sizes_file_name and write the result into big_bed_file_name
    :param sorted_bed_file_name:
    :param chrom_sizes_file_name:
    :param big_bed_file_name:
    :return:
    """

    # TODO: Move this into the _handleExceptionAndCheckCall function
    # Parse the array
    logging.debug("sorted_bed_file_name: {0}".format(sorted_bed_file_name))
    logging.debug("chrom_sizes_file_name: {0}".format(chrom_sizes_file_name))
    logging.debug("big_bed_file_name: {0}".format(big_bed_file_name))
    logging.debug("typeOption: {0}".format(typeOption))
    logging.debug("autoSql: {0}".format(autoSql))
    logging.debug("tab option: {0}".format(tab))

    array_call = ['bedToBigBed', sorted_bed_file_name, chrom_sizes_file_name, big_bed_file_name]
    if typeOption:
        typeOption = ''.join(['-type=', typeOption])
        array_call.append(typeOption)
    if autoSql:
        autoSql = ''.join(['-as=', autoSql])
        array_call.append(autoSql)
    if tab:
        array_call.append('-tab')

    p = _handleExceptionAndCheckCall(array_call)
    return p

def sortBam(input_bam_file_name, output_sorted_bam_name):
    """
    Call samtools on input_bam_file_name and output the result in output_sorted_bam_name
    :param input_bam_file_name:
    :param output_sorted_bam_name:
    :return:
    """
    array_call = ['samtools', 'sort', input_bam_file_name, '-o', output_sorted_bam_name]
    p = _handleExceptionAndCheckCall(array_call)
    return p

def createBamIndex(input_sorted_bam_file_name, output_name_index_name):
    """
    Call `samtools index` on imput_sorted_bam_file_name and output the result in output_name_index_name
    :param input_sorted_bam_file_name:
    :param output_name_index_name:
    :return:
    """
    array_call = ['samtools', 'index', input_sorted_bam_file_name, output_name_index_name]
    p = _handleExceptionAndCheckCall(array_call)
    return p

def pslToBigPsl(input_psl_file_name, output_bed12_file_name):
    """
    Call `pslToBigPsl` on input_psl_file_name and output the result in output_bed12_file_name
    :param input_psl_file_name: Name of the psl input file
    :param output_bed12_file_name: Name of the output file where to store the result of the cmd
    :return:
    """
    # The command to send
    array_call = ['pslToBigPsl', input_psl_file_name, output_bed12_file_name]

    p = _handleExceptionAndCheckCall(array_call)
    return p

#santitize trackName. Because track name must begin with a letter and
# contain only the following chars: [a-zA-Z0-9_].
# See the "track" Common settings at:
#https://genome.ucsc.edu/goldenpath/help/trackDb/trackDbHub.html#bigPsl_-_Pairwise_Alignments
def fixName(filename):
    if filename == 'cytoBandIdeo':
        return filename
    valid_chars = "_%s%s" % (string.ascii_letters, string.digits)
    sanitize_name = ''.join([c if c in valid_chars else '_' for c in filename])
    sanitize_name = "gonramp_" + sanitize_name
    return sanitize_name
