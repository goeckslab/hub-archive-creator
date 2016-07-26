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

def _handleExceptionAndCheckCall(array_call, **kwargs):
    """
    This class handle exceptions and call the tool.
    It maps the signature of subprocess.check_call:
    See https://docs.python.org/2/library/subprocess.html#subprocess.check_call
    """
    stdin = kwargs.get('stdin')
    stdout = kwargs.get('stdout')
    stderr = kwargs.get('stderr')
    shell = kwargs.get('shell')

    cmd = array_call[0]

    output = None
    error = None

    # TODO: Check the value of array_call and <=[0]
    logging.debug("Calling {0}:".format(cmd))

    #minus_to_add = ''.join('-' for x in range(len(cmd)))
    #logging.info("--------{0}".format(minus_to_add))
    logging.debug("---------")

    # TODO: Use universal_newlines option from Popen?
    try:
        p = subprocess.Popen(array_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        output, error = p.communicate()

        logging.debug("\t{0}".format(output))
        # If we detect an error from the subprocess, then we raise an exception
        # TODO: Manage if we raise an exception for everything, or use CRITICAL etc... but not stop process
        if p.returncode:
            #raise Exception(error)
            message = "The subprocess {0} has returned the error: {1}.".format(cmd, p.returncode)
            message = ''.join((message, " Its error message is: {0}".format(error)))
            logging.error(message)

            sys.exit(p.returncode)
    except OSError as e:
        message = "The subprocess {0} has encountered an OSError: {1}".format(cmd, e.strerror)
        if e.filename:
            message = ''.join((message, ", with this file: {0}".format(e.filename)))
        logging.error(message)
        sys.exit(-1)
    except Exception as e:
        message = "The subprocess {0} has encountered an error: {1}".format(cmd, e)
        logging.error(message)

        # TODO: More details for dev
        #raise Exception(message)
        logging.debug(e)

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


def bedToBigBed(sorted_bed_file_name, chrom_sizes_file_name, big_bed_file_name, typeOption=None, autoSql=None):
    """
    Call bedToBigBed on sorted_bed_file_name, using chrom_sizes_file_name and write the result into big_bed_file_name
    :param sorted_bed_file_name:
    :param chrom_sizes_file_name:
    :param big_bed_file_name:
    :return:
    """
    logging.debug("sorted_bed_file_name: {0}".format(sorted_bed_file_name))
    logging.debug("chrom_sizes_file_name: {0}".format(chrom_sizes_file_name))
    logging.debug("big_bed_file_name: {0}".format(big_bed_file_name))
    logging.debug("typeOption: {0}".format(typeOption))
    logging.debug("autoSql: {0}".format(autoSql))

    array_call = ['bedToBigBed', sorted_bed_file_name, chrom_sizes_file_name, big_bed_file_name]
    if typeOption:
        array_call.append(typeOption)
    if autoSql:
        array_call.append(autoSql)

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
