# -*- coding: utf-8 -*-

FILE_KEYS = ['path', 'directory', 'file']
#TABLE_KEYS = ['tracknumber', 'artist', 'title']
TABLE_KEYS = ['tracknumber', 'artist', 'title', 'date', 'album', 'comment']
TAG_KEYS = ['album', 'tracknumber', 'artist', 'title', 'date', 'comment']
FLACTAGS = ['ALBUM', 'TRACKNUMBER', 'ARTIST', 'TITLE', 'DATE', 'COMMENT']
MP3TAGS = ['TALB', 'TRCK', 'TPE1', 'TIT2', 'TDRC', 'COMM']
MP4TAGS = ['\xa9alb', 'trkn', '\xa9ART', '\xa9nam', '\xa9day', '\xa9cmt', ]
OGGTAGS = ['ALBUM', 'TRACKNUMBER', 'ARTIST', 'TITLE', 'DATE', 'COMMENT']

DEFAULT_ARTIST = 'Various Artists'

TRACK_SEPARATOR = '/'

DISALLOWED_CHARACTER_REPLACEMENT = u'\\'

EXTENSION_LIST = ['flac', 'mp3', 'mp4', 'm4a', 'm4b', 'm4p', 'ogg']
FLAC_EXTENSION = 'flac'
MP3_EXTENSION = 'mp3'
MP4_EXTENSION_LIST = ['mp4', 'm4a', 'm4b', 'm4p']
MP4_EXTENSION = 'mp4'
OGG_EXTENSION = 'ogg'

class AbstractModelType(object):
    #ModelType
    ModelTypeNone = 0
    ModelTypeFiles = 1
    ModelTypeTags = 2
    ModelTypeFree = 3
    ModelTypeFinal = 4
    def __init__(self):
        ''' 
        ''' 
        #self.log.debug('__init__ start')
        
        #self.log.debug('__init__ end')
        return None
    
    def getNameFromType(self, modelType):
        ''' 
        ''' 
        #self.log.debug('getNameFromType start')
        if modelType == 0:
            return 'ModelTypeNone'
        if modelType == 1:
            return 'ModelTypeFiles'
        if modelType == 2:
            return 'ModelTypeTags'
        if modelType == 3:
            return 'ModelTypeFree'
        if modelType == 4:
            return 'ModelTypeFinal'
        #self.log.debug('getNameFromType end')
        return 'unknown modelType'
    
ModelType = AbstractModelType()    
