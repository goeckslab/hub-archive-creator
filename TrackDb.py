#!/usr/bin/python
import collections
from util import santitizer

class TrackDb(object):
    """docstring for TrackDb"""
    def __init__(self, trackName="", longLabel="", shortLabel="", trackDataURL="", trackType="", extraSettings=None):
        #super(TrackDb, self).__init__()
        not_init_message = "The {0} is not initialized." 
        if trackName is None:
            raise TypeError(not_init_message.format('trackName'))
        if longLabel is None:
            raise TypeError(not_init_message.format('longLabel'))
        if trackType is None:
            raise TypeError(not_init_message.format('trackType'))
        if trackDataURL is None:
            raise TypeError(not_init_message.format('trackDataURL'))
            
        self.createTrackDb(trackName, longLabel, shortLabel, trackDataURL, trackType, extraSettings)

    def createTrackDb(self, track_name, long_label, short_label, file_path, track_type, extraSettings = None):
    
        # TODO: Remove the hardcoded "tracks" by the value used as variable from myTrackFolderPath
        data_url = "tracks/%s" % track_name
        if not short_label:
            short_label = TrackDb.getShortName(long_label)
        # Replace '_' by ' ', to invert the sanitization mecanism
        # TODO: Find a better way to manage the sanitization of file path
        long_label = long_label.replace("_", " ")
        short_label = short_label.replace("_", " ")

        #sanitize the track_name
        sanitized_name = santitizer.prefixTrackName(track_name)

        self.track_db = collections.OrderedDict([("track",sanitized_name),
                ("type",track_type),
                ("shortLabel",short_label),
                ("longLabel",long_label),
                ("bigDataUrl",data_url)]
                )
        
        
        TrackDb.prepareExtraSetting(extraSettings)
        self.track_db.update(extraSettings)
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
    def prepareExtraSetting(extraSettings):
        if not extraSettings:
            extraSettings = collections.OrderedDict()
        if not "color" in extraSettings:
            extraSettings["color"] = "#000000"
        extraSettings["color"] = TrackDb.getRgb(extraSettings["color"])
        if not "group" in extraSettings:
            extraSettings["group"] = "Default group"
        if not "thickDrawItem" in extraSettings:
            extraSettings["thickDrawItem"] = "off"
    
    def get(self, item_name):
        if item_name in self.track_db:
            return self.track_db[item_name]
        return None

    