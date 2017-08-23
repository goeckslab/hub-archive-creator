#!/usr/bin/python
from util import subtools

class TrackDb(object):
    """docstring for TrackDb"""
    def __init__(self, trackName="", longLabel="", shortLabel="", trackDataURL="", trackType="", extra_settings=None):
        super(TrackDb, self).__init__()
        self.createTrackDb(trackName, longLabel, shortLabel, trackDataURL, trackType, extra_settings)

    def createTrackDb(self, track_name, long_label, short_label, file_path, track_type, extra_settings = None):
    
        # TODO: Remove the hardcoded "tracks" by the value used as variable from myTrackFolderPath
        data_url = "tracks/%s" % track_name
        if not short_label:
            short_label = TrackDb.getShortName(long_label)
        # Replace '_' by ' ', to invert the sanitization mecanism
        # TODO: Find a better way to manage the sanitization of file path
        long_label = long_label.replace("_", " ")
        short_label = short_label.replace("_", " ")

        #sanitize the track_name
        sanitized_name = subtools.fixName(track_name)

        self.track_db = dict(trackName=sanitized_name,
                longLabel=long_label,
                shortLabel=short_label,
                trackDataURL=data_url,
                trackType=track_type
                )
        
        
        TrackDb.prepareExtraSetting(extra_settings)
        self.track_db.update(extra_settings)
        #print self.track_db

    # TODO: Rename for PEP8
    @staticmethod
    def getShortName(name_to_shortify):
        # Slice to get from Long label the short label
        short_label_slice = slice(0, 17)
        return name_to_shortify[short_label_slice]

    @staticmethod
    def getRgb(track_color):
        #TODO: Check if rgb or hexa
        # Convert hexa to rgb array
        hexa_without_sharp = track_color.lstrip('#')
        rgb_array = [int(hexa_without_sharp[i:i+2], 16) for i in (0, 2, 4)]
        rgb_ucsc = ','.join(map(str, rgb_array))
        return rgb_ucsc

    @staticmethod
    def prepareExtraSetting(extra_settings):
        if not extra_settings:
            extra_settings = dict()
        if not "track_color" in extra_settings:
            extra_settings["track_color"] = "#000000"
        extra_settings["track_color"] = TrackDb.getRgb(extra_settings["track_color"])
        if not "group_name" in extra_settings:
            extra_settings["group_name"] = "Default"
        if not "thick_draw_item" in extra_settings:
            extra_settings["thickDrawItem"] = "off"
    
    def get(self, item_name):
        return self.track_db[item_name]
'''
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
'''            