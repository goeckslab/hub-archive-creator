#!/usr/bin/python

class TrackDb(object):
    """docstring for TrackDb"""

    def __init__(self, trackName="", longLabel="", shortLabel="", trackDataURL="", trackType="", visibility="",
                 thickDrawItem='off', priority="0", track_color="#000000", group_name="Default", database=""):
        super(TrackDb, self).__init__()

        self.trackName = trackName
        self.longLabel = longLabel
        self.shortLabel = shortLabel
        self.trackDataURL = trackDataURL
        self.trackType = trackType
        self.visibility = visibility
        self.thickDrawItem = thickDrawItem
        self.priority = priority
        self.track_color = track_color
        self.group_name = group_name
        self.database = database
            