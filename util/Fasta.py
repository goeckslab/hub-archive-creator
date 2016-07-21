#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Class describing the Fasta format
(As of the 07/20/2016, only used with the reference genome)
"""

class Fasta(object):
    def __init__(self, false_path, name, assembly_id):
        self.false_path = false_path
        self.name = name
        self.assembly_id = assembly_id