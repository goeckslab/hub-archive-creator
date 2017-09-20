#!/usr/bin/python
import collections
import abc
from abc import ABCMeta

class ExternIndex(object):
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def __init__(self):
        """init"""
    
    @abc.abstractmethod
    def setExtLink(self):
        """set external link"""
        
    
    

    '''
    @staticmethod 
    def setExtLink(database, inputFile, extra_settings, seqType=None, useIframe=True, iframeHeight=None, iframeWidth=None):
        if "NCBI" in database:
            if not seqType:
                seqType = int(ExternIndex.getSeqType(inputFile))
            else:
                seqType = seqType
            if seqType < 0:
                print seqType
                raise Exception("Sequence Type is not set for bigPsl. Stopping the application")
            if seqType == 2:
                extra_settings["url"] = "https://www.ncbi.nlm.nih.gov/protein/$$"
            elif seqType == 1:
                extra_settings["url"] = "https://www.ncbi.nlm.nih.gov/nuccore/$$"
            else:
                raise Exception("Sequence Type {0} is not valid for bigPsl. Stopping the application".format(seqType))
        elif "UniProt" in database:
            extra_settings["url"] = "http://www.uniprot.org/uniprot/$$"
        elif "FlyBase" in database:
            extra_settings["url"] = "http://flybase.org/reports/$$"
        else:
            extra_settings["url"] = "https://www.ncbi.nlm.nih.gov/gquery/?term=$$"
        extra_settings["urlLabel"] = database + " Details:"
        if useIframe:
            extra_settings["iframeUrl"] = extra_settings["url"]
            if not iframeHeight:
                iframeHeight = "600"
            if not iframeWidth:
                iframeWidth = "800"
            extra_settings["iframeOptions"] = "height= %s width= %s" % (iframeHeight, iframeWidth)

    @staticmethod
    def getSeqType(inputFile):
        with open(inputFile, "r") as bigpsl:
            sampleSeq = bigpsl.readline().split()
        if len(sampleSeq) == 25:
            return sampleSeq[-1]
        else:
            return "-1"        
    '''