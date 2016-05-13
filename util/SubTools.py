#!/usr/bin/python

"""
This class handles the subprocess calls of the different tools used
in HubArchiveCreator
"""

import os
import subprocess


class SubTools(object):
    def __init__(self):
        super(SubTools, self).__init__()

    def __handleExceptionAndCheckCall__(self, array_call, **kwargs):
        """
        This class handle exceptions and call the tool.
        It maps the signature of subprocess.check_call:
        See https://docs.python.org/2/library/subprocess.html#subprocess.check_call
        """
        stdin = kwargs.get('stdin')
        stdout = kwargs.get('stdout')
        stderr = kwargs.get('stderr')
        shell = kwargs.get('shell')
        try:
            p = subprocess.check_call(array_call, stdin=stdin, stdout=stdout, stderr=stderr, shell=shell)
        except subprocess.CalledProcessError:
            raise
        return p

    def twoBitInfo(self, two_bit_file_name, two_bit_info_file):
        """
        Call twoBitInfo and write the result into twoBit_info_file
        :param two_bit_file_name:
        :param two_bit_info_file:
        :return the subprocess.check_call return object:
        """
        array_call = ['twoBitInfo', two_bit_file_name, two_bit_info_file]
        p = self.__handleExceptionAndCheckCall__(array_call)
        return p

    def faToTwoBit(self, fasta_file_name, mySpecieFolder):
        """
        This function call faToTwoBit UCSC tool, and return the twoBitFile
        :param fasta_file_name:
        :param mySpecieFolder:
        :return:
        """
        baseNameFasta = os.path.basename(fasta_file_name)
        suffixTwoBit, extensionTwoBit = os.path.splitext(baseNameFasta)
        nameTwoBit = suffixTwoBit + '.2bit'

        with open(os.path.join(mySpecieFolder, nameTwoBit), 'w') as twoBitFile:
            array_call = ['faToTwoBit', fasta_file_name, twoBitFile.name]
            self.__handleExceptionAndCheckCall__(array_call)

        return twoBitFile

    def gff3ToGenePred(self, input_gff3_file_name, gene_pred_file_name):
        """
        Call gff3ToGenePred and write the result into gene_pred_file_name
        :param input_gff3_file_name:
        :param gene_pred_file_name:
        :return:
        """
        array_call = ['gff3ToGenePred', input_gff3_file_name, gene_pred_file_name]
        p = self.__handleExceptionAndCheckCall__(array_call)
        return p

    def genePredToBed(self, gene_pred_file_name, unsorted_bed_file_name):
        """
        Call genePredToBed and write the result into unsorted_bed_file_name
        :param gene_pred_file_name:
        :param unsorted_bed_file_name:
        :return:
        """
        array_call = ['genePredToBed', gene_pred_file_name, unsorted_bed_file_name]
        p = self.__handleExceptionAndCheckCall__(array_call)
        return p

    def sort(self, unsorted_bed_file_name, sorted_bed_file_name):
        """
        Call sort with -k1,1 -k2,2n on unsorted_bed_file_name and write the result into sorted_bed_file_name
        :param unsorted_bed_file_name:
        :param sorted_bed_file_name:
        :return:
        """
        array_call = ['sort', '-k', '1,1', '-k', '2,2n', unsorted_bed_file_name, '-o', sorted_bed_file_name]
        p = self.__handleExceptionAndCheckCall__(array_call)
        return p

    def sortChromSizes(self, two_bit_info_file_name, chrom_sizes_file_name):
        """
        Call sort with -k2rn on two_bit_info_file_name and write the result into chrom_sizes_file_name
        :param two_bit_info_file_name:
        :param chrom_sizes_file_name:
        :return:
        """
        array_call = ['sort', '-k2rn', two_bit_info_file_name, '-o', chrom_sizes_file_name]
        p = self.__handleExceptionAndCheckCall__(array_call)
        return p

    def bedToBigBed(self, sorted_bed_file_name, chrom_sizes_file_name, big_bed_file_name, typeOption=None, autoSql=None):
        """
        Call bedToBigBed on sorted_bed_file_name, using chrom_sizes_file_name and write the result into big_bed_file_name
        :param sorted_bed_file_name:
        :param chrom_sizes_file_name:
        :param big_bed_file_name:
        :return:
        """
        array_call = ['bedToBigBed', sorted_bed_file_name, chrom_sizes_file_name, big_bed_file_name]
        if typeOption:
            array_call.append(typeOption)
        if autoSql:
            array_call.append(autoSql)

        p = self.__handleExceptionAndCheckCall__(array_call)
        return p