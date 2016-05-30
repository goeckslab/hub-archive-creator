#!/usr/bin/python


class Track(object):
    """Class to manage the track informations needed for Track Hub, in the TrackDb text file"""

    def __init__(self, trackFile=None, trackDb=None):
        self.trackFile = trackFile

        self.trackDb = trackDb
