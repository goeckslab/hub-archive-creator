#!/usr/bin/python


class Track(object):
    """Class to manage the track informations needed for Track Hub, in the TrackDb text file"""
    def __init__(self, trackFile=None, trackName=None, longLabel=None, shortLabel=None, trackDataURL=None, trackType=None, visibility=None, thickDrawItem='off'):
        self.trackFile = trackFile
        self.trackName = trackName
        self.longLabel = longLabel
        self.shortLabel = shortLabel
        self.trackDataURL = trackDataURL
        self.trackType = trackType
        self.visibility = visibility
        self.thickDrawItem = thickDrawItem
