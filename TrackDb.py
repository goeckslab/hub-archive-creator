#!/usr/bin/python

class TrackDb(object):
    """docstring for TrackDb"""

    def __init__(self, trackName="", longLabel="", shortLabel="", trackDataURL="", trackType="", visibility="",
                 thickDrawItem='off'):
        super(TrackDb, self).__init__()

        self.trackName = trackName
        self.longLabel = longLabel
        self.shortLabel = shortLabel
        self.trackDataURL = trackDataURL
        self.trackType = trackType
        self.visibility = visibility
        self.thickDrawItem = thickDrawItem
