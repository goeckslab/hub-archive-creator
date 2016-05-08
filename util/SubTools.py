#!/usr/bin/python

"""
This class handles the subprocess calls of the different tools used
in HubArchiveCreator
"""

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