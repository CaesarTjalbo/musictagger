# -*- coding: utf-8 -*-
import os
import logging
import time

import re
import copy

from PyQt4.QtCore import QString

import tags
import utils_module
import model_classes
import constants

'''
keys
albumArtist
albumTitle
albumDate
modelType
rows
    path
    directory
    file
    album
    tracknumber
    artist
    title
    date
    comment
'''

class Album(object):
    
    #tags = tags.Tags()
    #keys = ['path', 'directory', 'file', 'tracknumber', 'title', 'artist', 'album', 'date']
    _albumArtist = ''          # property albumArtist
    _albumTitle = ''           # property albumTitle
    _albumDate = ''            # property albumDate
    _directory = None           # property directory
    _fullDirectory = None           # property fullDirectory
    _albumComment = ''          # property albumComment
    
    _albumArtistFromFile = None
    _albumArtistFromTag = None
    _albumArtistFromFree = None
    
    _albumTitleFromFile = None
    _albumTitleFromTag = None
    _albumTitleFromFree = None
    
    _albumDateFromFile = None
    _albumDateFromTag = None
    _albumDateFromFree = None
    
    #_Model = None               # property Model
    _modelType = constants.ModelType.ModelTypeNone
    
    _useAlbumArtist = False # force a single artist on every track
    _useAlbumDate = False # force a date on every track
    _useAlbumTitle = False # force an albumTitle on every track
    _useAlbumComment = False # force a comment
    _useAlbumVariousArtists = False # set artist in directory to "Various Artists"
    #_useAlbumArtist = None
    #_useAlbumDate = None
    #_useAlbumTitle = None
    _volumeString = ''
    
    _qtparent = None
    
    tag_rows = list() # contains data per song based on tags
    file_rows = list() # contains data per song based on files
    rows = list()
    
    stored_rows = list()
    storedAlbumArtist = ''
    storedAlbumTitle = ''
    storedAlbumDate = ''
    
    #model = None
    
    tagProcessor = tags.Tags()
    utils = utils_module.Utils()
    
    def __init__(self, qtparent):
        ''' 
        ''' 
        self.log = logging.getLogger('Album')
        self._qtparent = qtparent
        #self.log.debug('__init__ start')
        self.rows = list()
        self.tag_rows = list()
        self.file_rows = list()
        
        #self.log.debug('__init__ end')
        return None
    
    def _setAlbumArtist(self, value):
        ''' '''
        #
        self._albumArtist = unicode(value)
        if self.model:
            if self.modelType == constants.ModelType.ModelTypeNone:
                pass
            if self.modelType == constants.ModelType.ModelTypeTags:
                pass
            if self.modelType == constants.ModelType.ModelTypeFiles:
                pass
            if self.modelType == constants.ModelType.ModelTypeFree:
                self._albumArtistFromFree = unicode(value)
        #
        return None
        
    def _getAlbumArtist(self):
        ''' '''
        #self.log.debug('_getAlbumArtist start')
        if self.modelType == constants.ModelType.ModelTypeFiles:
            return self._albumArtistFromFile
        if self.modelType == constants.ModelType.ModelTypeTags:
            return self._albumArtistFromTag
        if self.modelType == constants.ModelType.ModelTypeFree:
            return self._albumArtistFromFree
        #self.log.debug('_getAlbumArtist end')
        return self._albumArtist
        
    albumArtist = property(_getAlbumArtist, _setAlbumArtist)
            
    def _setAlbumTitle(self, value):
        ''' '''
        #self.log.debug('_setAlbumTitle start')
        self._albumTitle = unicode(value)
        if self.model:
            if self.modelType == constants.ModelType.ModelTypeNone:
                pass
            if self.modelType == constants.ModelType.ModelTypeTags:
                pass
            if self.modelType == constants.ModelType.ModelTypeFiles:
                pass
            if self.modelType == constants.ModelType.ModelTypeFree:
                self._albumTitleFromFree = unicode(value)
        #self.log.debug('_setAlbumTitle end')
        return None
        
    def _getAlbumTitle(self):
        ''' '''
        #self.log.debug('_getAlbumTitle start')
        if self.modelType == constants.ModelType.ModelTypeFiles:
            return self._albumTitleFromFile
        if self.modelType == constants.ModelType.ModelTypeTags:
            return self._albumTitleFromTag
        if self.modelType == constants.ModelType.ModelTypeFree:
            return self._albumTitleFromFree
        #self.log.debug('_getAlbumTitle end')
        return self._albumTitle
        
    albumTitle = property(_getAlbumTitle, _setAlbumTitle)
                    
    def _setAlbumDate(self, value):
        ''' '''
        #self.log.debug('_setAlbumDate start')
        self._albumDate = unicode(value)
        if self.model:
            if self.modelType == constants.ModelType.ModelTypeNone:
                pass
            if self.modelType == constants.ModelType.ModelTypeTags:
                pass
            if self.modelType == constants.ModelType.ModelTypeFiles:
                pass
            if self.modelType == constants.ModelType.ModelTypeFree:
                self._albumDateFromFree = unicode(value)
        #self.log.debug('_setAlbumDate end')
        return None
        
    def _getAlbumDate(self):
        ''' '''
        #self.log.debug('_getAlbumDate start')
        if self.modelType == constants.ModelType.ModelTypeFiles:
            return self._albumDateFromFile
        if self.modelType == constants.ModelType.ModelTypeTags:
            return self._albumDateFromTag
        if self.modelType == constants.ModelType.ModelTypeFree:
            return self._albumDateFromFree
        #self.log.debug('_getAlbumDate end')
        return self._albumDate
        
    albumDate = property(_getAlbumDate, _setAlbumDate)
                            
    def _setAlbumComment(self, value):
        ''' '''
        #self.log.debug('_setAlbumComment start')
        self._albumComment = unicode(value)
        #self.log.debug('_setAlbumComment end')
        return None
        
    def _getAlbumComment(self):
        ''' '''
        #self.log.debug('_getAlbumComment start')
        #self.log.debug('_getAlbumDate end')
        return self._albumComment
        
    albumComment = property(_getAlbumComment, _setAlbumComment)
                            
    def _setAlbumArtistFromFile(self, value):
        ''' '''
        #self.log.debug('_setAlbumArtistFromFile start')
        self._albumArtistFromFile = value
        #self.log.debug('_setAlbumArtistFromFile end')
        return None
        
    def _getAlbumArtistFromFile(self):
        ''' '''
        #self.log.debug('_getAlbumArtistFromFile start')
        #self.log.debug('_getAlbumArtistFromFile start')
        return self._albumArtistFromFile
        
    def _setAlbumArtistFromTag(self, value):
        ''' '''
        #self.log.debug('_setAlbumArtistFromTag start')
        self._albumArtistFromTag = value
        #self.log.debug('_setAlbumArtistFromTag end')
        return None
        
    def _getAlbumArtistFromTag(self):
        ''' '''
        #self.log.debug('_getAlbumArtistFromTag start')
        #self.log.debug('_getAlbumArtistFromTag start')
        return self._albumArtistFromTag
        
    def _setAlbumArtistFromFree(self, value):
        ''' '''
        #self.log.debug('_setAlbumArtistFromFree start')
        self._albumArtistFromFree = value
        #self.log.debug('_setAlbumArtistFromFree end')
        return None
        
    def _getAlbumArtistFromFree(self):
        ''' '''
        #self.log.debug('_getAlbumArtistFromFree start')
        #self.log.debug('_getAlbumArtistFromFree start')
        return self._albumArtistFromFree
        
    def _setAlbumTitleFromFile(self, value):
        ''' '''
        #self.log.debug('_setAlbumTitleFromFile start')
        self._albumTitleFromFile = value
        #self.log.debug('_setAlbumTitleFromFile end')
        return None
        
    def _getAlbumTitleFromFile(self):
        ''' '''
        #self.log.debug('_getAlbumTitleFromFile start')
        #self.log.debug('_getAlbumTitleFromFile start')
        return self._albumTitleFromFile
        
    def _setAlbumTitleFromTag(self, value):
        ''' '''
        #self.log.debug('_setAlbumTitleFromTag start')
        self._albumTitleFromTag = value
        #self.log.debug('_setAlbumTitleFromTag end')
        return None
        
    def _getAlbumTitleFromTag(self):
        ''' '''
        #self.log.debug('_getAlbumTitleFromTag start')
        #self.log.debug('_getAlbumTitleFromTag start')
        return self._albumTitleFromTag
        
    def _setAlbumTitleFromFree(self, value):
        ''' '''
        #self.log.debug('_setAlbumTitleFromFree start')
        self._albumTitleFromFree = value
        #self.log.debug('_setAlbumTitleFromFree end')
        return None
        
    def _getAlbumTitleFromFree(self):
        ''' '''
        #self.log.debug('_getAlbumTitleFromFree start')
        #self.log.debug('_getAlbumTitleFromFree start')
        return self._albumTitleFromFree
        
    def _setAlbumDateFromFile(self, value):
        ''' '''
        #self.log.debug('_setAlbumDateFromFile start')
        self._albumDateFromFile = value
        #self.log.debug('_setAlbumDateFromFile end')
        return None
        
    def _getAlbumDateFromFile(self):
        ''' '''
        #self.log.debug('_getAlbumDateFromFile start')
        #self.log.debug('_getAlbumDateFromFile start')
        return self._albumDateFromFile
        
    def _setAlbumDateFromTag(self, value):
        ''' '''
        #self.log.debug('_setAlbumDateFromTag start')
        self._albumDateFromTag = value
        #self.log.debug('_setAlbumDateFromTag end')
        return None
        
    def _getAlbumDateFromTag(self):
        ''' '''
        #self.log.debug('_getAlbumDateFromTag start')
        #self.log.debug('_getAlbumDateFromTag start')
        return self._albumDateFromTag
    
    def _setAlbumDateFromFree(self, value):
        ''' '''
        #self.log.debug('_setAlbumDateFromFree start')
        self._albumDateFromFree = value
        #self.log.debug('_setAlbumDateFromFree end')
        return None
        
    def _getAlbumDateFromFree(self):
        ''' '''
        #self.log.debug('_getAlbumDateFromFree start')
        #self.log.debug('_getAlbumDateFromFree start')
        return self._albumDateFromFree
    
    def _setUseAlbumArtist(self, value):
        ''' 
        ''' 
        #self.log.debug('_setUseAlbumArtist start')
        self._useAlbumArtist = value
        if value:
            for row in self.rows:
                row['artist'] = self.albumArtist
        #self.log.debug('_setUseAlbumArtist end')
        return None
    
    def _getUseAlbumArtist(self):
        ''' 
        ''' 
        #self.log.debug('_getUseAlbumArtist start')
        
        #self.log.debug('_getUseAlbumArtist end')
        return self._useAlbumArtist
    
    useAlbumArtist = property(_getUseAlbumArtist, _setUseAlbumArtist)
    
    def _setUseAlbumTitle(self, value):
        ''' 
        ''' 
        #self.log.debug('_setUseAlbumTitle start')
        self._useAlbumTitle = value
        if value:
            for row in self.rows:
                row['album'] = self.albumTitle
        #self.log.debug('_setUseAlbumTitle end')
        return None
    
    def _getUseAlbumTitle(self):
        ''' 
        ''' 
        #self.log.debug('_getUseAlbumTitle start')
        
        #self.log.debug('_getUseAlbumTitle end')
        return self._useAlbumTitle
    
    useAlbumTitle = property(_getUseAlbumTitle, _setUseAlbumTitle)
    
    def _setUseAlbumDate(self, value):
        ''' 
        ''' 
        #self.log.debug('_setUseAlbumDate start')
        self._useAlbumDate = value
        if value:
            for row in self.rows:
                row['date'] = self.albumDate
        #self.log.debug('_setUseAlbumDate end')
        return None
    
    def _getUseAlbumDate(self):
        ''' 
        ''' 
        #self.log.debug('_getUseAlbumDate start')
        
        #self.log.debug('_getUseAlbumDate end')
        return self._useAlbumDate
    
    useAlbumDate = property(_getUseAlbumDate, _setUseAlbumDate)
    
    def _setUseAlbumComment(self, value):
        ''' 
        ''' 
        #self.log.debug('_setUseAlbumComment start')
        self._useAlbumComment = value
        if value:
            for row in self.rows:
                row['comment'] = self.albumComment
        #self.log.debug('_setUseAlbumComment end')
        return None
    
    def _getUseAlbumComment(self):
        ''' 
        ''' 
        #self.log.debug('_getUseAlbumComment start')
        
        #self.log.debug('_getUseAlbumComment end')
        return self._useAlbumComment
    
    useAlbumComment = property(_getUseAlbumComment, _setUseAlbumComment)
    
    def _setUseAlbumVariousArtists(self, value):
        ''' 
        ''' 
        #self.log.debug('_setUseAlbumVariousArtists start')
        self._useAlbumVariousArtists = value
        self._qtparent.blah('gghjgj')
        #self.log.debug('_setUseAlbumVariousArtists end')
        return None
    
    def _getUseAlbumVariousArtists(self):
        ''' 
        ''' 
        #self.log.debug('_getUseAlbumVariousArtists start')
        
        #self.log.debug('_getUseAlbumVariousArtists end')
        return self._useAlbumVariousArtists
    
    useAlbumVariousArtists = property(_getUseAlbumVariousArtists, _setUseAlbumVariousArtists)
    
    def _setUseAlbumContinuousNumbering(self, value):
        ''' ''' 
        #self.log.debug('_setUseAlbumContinuousNumbering start')
        self._useAlbumContinuousNumbering = value
        if value:
            for i, row in enumerate(self.rows):
                row['tracknumber'] = unicode(i + 1)
        #self.log.debug('_setUseAlbumContinuousNumbering end')
        return None
    
    def _getUseAlbumContinuousNumbering(self):
        ''' ''' 
        #self.log.debug('_getUseAlbumContinuousNumbering start')
        
        #self.log.debug('_getUseAlbumContinuousNumbering end')
        return self._useAlbumContinuousNumbering
    
    useAlbumContinuousNumbering = property(_getUseAlbumContinuousNumbering, _setUseAlbumContinuousNumbering)
    
    def _setDirectory(self, value):
        ''' '''
        #self.log.debug('_setDirectory start')
        self._directory = unicode(value)
        #self.log.debug('_setDirectory end')
        return None
        
    def _getDirectory(self):
        ''' '''
        #self.log.debug('_getDirectory start')
        #self.log.debug('_getDirectory end')
        return self._directory
        
    directory = property(_getDirectory, _setDirectory)

    def _setFullDirectory(self, value):
        ''' '''
        #self.log.debug('_setFullDirectory start')
        self._fullDirectory = unicode(value)
        #self.log.debug('_setFullDirectory end')
        return None
        
    def _getFullDirectory(self):
        ''' '''
        #self.log.debug('_getFullDirectory start')
        #self.log.debug('_getFullDirectory end')
        return self._fullDirectory
        
    fullDirectory = property(_getFullDirectory, _setFullDirectory)

    def _getVolumeString(self):
        ''' ''' 
        #log = logging.getLogger('%s._getVolumeString' % self.log.name)
        #self.log.debug('_getVolumeString start')
        
        #self.log.debug('_getVolumeString end')
        return self._volumeString
    
    def _setVolumeString(self, value):
        ''' ''' 
        #log = logging.getLogger('%s._setVolumeString' % self.log.name)
        #self.log.debug('_setVolumeString start')
        self._volumeString = value
        #self.log.debug('_setVolumeString end')
        return None
    
    volumeString = property(_getVolumeString, _setVolumeString)
    
    #def _getModel(self):
        #''' 
        #''' 
        ##self.log.debug('_getModel start')
        ##self.log.debug('_getModel end')
        #return self._Model
    
    #def _setModel(self, model):
        #''' 
        #''' 
        ##self.log.debug('_setModel start')
        #self._Model = model
        ##self.log.debug('_setModel end')
        #return None
    
    #Model = property(_getModel, _setModel)
    
    #def _setModelType(self, value):
        #''' '''
        ##self.log.debug('_setModelType start')
        #if self.Model:
            #self.Model.modelType = value
        #self._modelType = value
        ##self.log.debug('_setModelType end')
        #return None
        
    def _getModelType(self):
        ''' '''
        #self.log.debug('_getModelType start')
        if self.model:
            return self.model.modelType
        #self.log.debug('_getModelType end')
        return constants.ModelType.ModelTypeNone
        
    modelType = property(_getModelType)#, _setModelType)
        
    def setFileAndTagData(self, fileDataList):
        ''' import all the data
        ''' 
        #self.log.debug('setFileAndTagData start')
        # store all data in self.rows
        # all data for tags in self.tag_rows
        # all data for file in self. file_rows
        
        self.rows = list()
        
        # before starting to loop, get some data for the file info
        directoryResult = self.utils.getAlbumDataFromDirectoryName(self.directory)
        
        # helper variables to determine albumArtist, albumDate, albumTitle from tags
        allAlbumTitlesFromTags = list()
        allAlbumArtistsFromTags = list()
        allAlbumDatesFromTags = list()
        
        for fileData in fileDataList:
            #self.log.debug(fileData)
            row_dict = dict()
            
            # determine filename, extension, path
            filename = unicode(fileData['file'])
            extension = ''
            for extension in constants.EXTENSION_LIST:
                if filename[- (len(extension) + 1): ] == '.%s' % extension:
                    break
            
            path = fileData['path']
            
            tagResult = self.getTagsFromFile(fileData['path'])
            for key in tagResult.keys():
                tagResult[key] = tagResult[key]
            
            # add the data from tags to self.rows
            for k in tagResult.keys():
                row_dict[k] = tagResult[k]
            #self.log.debug(row_dict)
            
            tagResult['filename'] = filename
            tagResult['path'] = path
            tagResult['extension'] = extension
            self.tag_rows.append(tagResult)
            
            if 'album' in tagResult.keys():
                allAlbumTitlesFromTags.append(tagResult['album'])
            if 'artist' in tagResult.keys():
                allAlbumArtistsFromTags.append(tagResult['artist'])
            if 'date' in tagResult.keys():
                allAlbumDatesFromTags.append(tagResult['date'])
            
            
            ################################ now for data from files
            fileResult = self.utils.getSongDataFromFileName(fileData['file'])
            
            # add the data from tags to self.rows, *now* to prevent overwriting data from tags
            for key in fileResult.keys():
                row_dict[key] = fileResult[key]
            #self.log.debug(row_dict)
            
            fileResult['filename'] = filename
            fileResult['path'] = path
            fileResult['extension'] = extension
            fileResult['album'] = directoryResult['album']
            fileResult['date'] = directoryResult['date']
            for key in constants.TABLE_KEYS:
                if key in fileResult.keys():
                    pass
                else:
                    fileResult[key] = u''
            
            self.file_rows.append(fileResult)
            
            self.rows.append(row_dict)
            
            #self.log.debug(len(fileResult))
            #self.log.debug(len(tagResult))
            #self.log.debug(fileResult)
            #self.log.debug(tagResult)
        
        # try to find data for ModelTypeTags
        self._albumTitleFromTag = self.utils.getUniqueStringFromList(allAlbumTitlesFromTags)
        self._albumArtistFromTag = self.utils.getUniqueStringFromList(allAlbumArtistsFromTags)
        self._albumDateFromTag = self.utils.getUniqueStringFromList(allAlbumDatesFromTags)
        
        # using data from the directory name for ModelTypeFree and ModelTypeFiles
        self._albumTitleFromFree = self._albumTitleFromFile = directoryResult['album']
        self._albumArtistFromFree = self._albumArtistFromFile = directoryResult['artist']
        self._albumDateFromFree = self._albumDateFromFile = directoryResult['date']
        #self.log.debug('setFileAndTagData end')
        return None
    
    #def processTags(self, fileDataList):
        #''' 
        #''' 
        ##self.log.debug('processTags start')
        ## helper variables to determine albumArtist, albumDate, albumTitle from tags
        #allAlbumTitlesFromTags = list()
        #allAlbumArtistsFromTags = list()
        #allAlbumDatesFromTags = list()
        
        #for fileData in fileDataList:
            ##self.log.debug(fileData)
            ####row_dict = dict()
            
            ## determine filename, extension, path
            #filename = unicode(fileData['file'])
            #if filename[-4:].lower() == '.mp3':
                ##tag_dict['extension'] = '.mp3'
                #extension = '.mp3'
            #elif filename[-5:].lower() == '.flac':
                ##tag_dict['extension'] = u'.flac'
                #extension = u'.flac'
            #else:
                ##tag_dict['extension'] = u'unknown'
                #extension = u'unknown'
            #path = fileData['path']
            
            #tagResult = self.getTagsFromFile(fileData['path'])
            #for key in tagResult.keys():
                #tagResult[key] = tagResult[key]
            
            #### add the data from tags to self.rows
            ###for k in tagResult.keys():
                ###row_dict[k] = tagResult[k]
            ####self.log.debug(row_dict)
            
            #tagResult['filename'] = filename
            #tagResult['path'] = path
            #tagResult['extension'] = extension
            #self.tag_rows.append(tagResult)
            
            #if 'album' in tagResult.keys():
                #allAlbumTitlesFromTags.append(tagResult['album'])
            #if 'artist' in tagResult.keys():
                #allAlbumArtistsFromTags.append(tagResult['artist'])
            #if 'date' in tagResult.keys():
                #allAlbumDatesFromTags.append(tagResult['date'])
                
        #self._albumTitleFromTag = self.utils.getUniqueStringFromList(allAlbumTitlesFromTags)
        #self._albumArtistFromTag = self.utils.getUniqueStringFromList(allAlbumArtistsFromTags)
        #self._albumDateFromTag = self.utils.getUniqueStringFromList(allAlbumDatesFromTags)
        
        ##self.log.debug('processTags end')
        #return None
    
    def getTagsFromFile(self, path):
        ''' 
        ''' 
        #self.log.debug('getTagsFromFile start')
        #self.log.debug('getTagsFromFile end')
        return self.tagProcessor.readFile(path)
    
    def getModelClass(self, modelType):
        ''' 
        ''' 
        #self.log.debug('getModelClass start')
        if modelType == constants.ModelType.ModelTypeNone:
            self.model = self._getModelClassNone()
            
        if modelType == constants.ModelType.ModelTypeFiles:
            self.model = self._getModelClassFiles()
            
        if modelType == constants.ModelType.ModelTypeTags:
            self.model = self._getModelClassTags()
            
        if modelType == constants.ModelType.ModelTypeFree:
            self.model = self._getModelClassFree()
            
        if modelType == constants.ModelType.ModelTypeFinal:
            if hasattr(self, 'model') and self.model:
                self.model = self._getModelClassFinal(self.model)
        
        if hasattr(self, 'model') and self.model:
            self.model.album = self
        else:
            self.log.error('No Model through getModelClass, type = %s' % constants.ModelType.getNameFromType(modelType))
            # is ok, screen can handle None
            # SHOULDN'T happen anymore  (happened when a directory is selected without mp3/flac in it and user jumps to final screen)
            self.model = self._getModelClassNone()
        #self.log.debug('getModelClass end')
        return self.model
    
    def _getModelClassNone(self):
        ''' 
        ''' 
        #self.log.debug('_getModelClassNone start')
        model = model_classes.Model(self._qtparent)
        model.keys = constants.TABLE_KEYS
        model.modelType = constants.ModelType.ModelTypeNone
        self.rows = list()
        #self.log.debug('_getModelClassNone end')
        return model
    
    def _getModelClassFiles(self):
        ''' 
        ''' 
        #self.log.debug('_getModelClassFiles start')
        model = model_classes.Model(self._qtparent)
        model.keys = constants.TABLE_KEYS
        model.modelType = constants.ModelType.ModelTypeFiles
        self.rows = copy.deepcopy(self.file_rows)
        
        #self.log.debug('_getModelClassFiles end')
        return model
        
    def _getModelClassTags(self):
        ''' 
        ''' 
        #self.log.debug('_getModelClassTags start')
        model = model_classes.Model(self._qtparent)
        model.keys = constants.TABLE_KEYS
        model.modelType = constants.ModelType.ModelTypeTags
        self.rows = copy.deepcopy(self.tag_rows)
        
        #self.log.debug('_getModelClassTags end')
        return model
    
    def _getModelClassFree(self):
        ''' ModelType with data from the 'free' tab
        this model is different because the data doesn't arrive until the user moves to the final tab
        ''' 
        #self.log.debug('_getModelClassFree start')
        model = model_classes.Model(self._qtparent)
        model.keys = constants.TABLE_KEYS
        model.modelType = constants.ModelType.ModelTypeFree
        keys = ['album', 'comment', 'title', 'artist', 'date', 'tracknumber']
        self.rows = copy.deepcopy(self.tag_rows)
        for row in self.rows:
            for key in keys:
                row[key] = u''
        #self.log.debug(self.albumArtist)
        #self.log.debug(self.albumTitle)
        #self.log.debug(self.albumDate)
        #self.log.debug(
        #self.rows = list()
        #self.log.debug('_getModelClassFree end')
        return model
    
    def _getModelClassFinal(self, previousModel):
        ''' copy of the last model with the ModelType = ModelTypeFinal
        store the settings so a reset of the data can be done
        ''' 
        #self.log.debug('_getModelClassFinal start')

        # hack: these property return based on modelType, need to set before changing modelType
        self.albumArtist = self.albumArtist
        self.albumTitle = self.albumTitle
        self.albumDate = self.albumDate
        self._storeAlbumAttributes()
        previousModel.modelType = constants.ModelType.ModelTypeFinal
        #self.log.debug('_getModelClassFinal end')
        return previousModel
    
    
    def save(self):
        ''' 
        ''' 
        #self.log.debug('save start')
        #self.log.debug('***********************************************************************************')
        
        FOR_REAL = True
        #FOR_REAL = False
        #for row in self.rows:
            #self.log.debug(row)
        #test = 4
        
        #if test == 0:
            #self.log.debug(constants.TAG_KEYS)
            #for i, row in enumerate(self.rows):
                #self.log.debug(row)
                
        #if test == 1:
            #self._saveTags()
        
        #if test == 2:
            #self._saveFileNames()
        
        #if test == 3:
            #self._saveDirectory()
        
        self._qtparent.showSaveDialog()
        
        result = True
        self._exec_chmod()
        result = self._saveTags(FOR_REAL)
        
        if not result:
            self.log.debug('something failed writing tags')

        result = self._saveFileNames(FOR_REAL)
        
        newDirectoryName = ''
        if not result:
            self.log.debug('something failed writing file names')
        
        result, newDirectoryName = self._saveDirectory(FOR_REAL)
        if not result:
            self.log.debug('something failed renaming directory')
        #self.log.debug('save end')
        #return True, self.fullDirectory
        return result, newDirectoryName
        #self.log.debug('***********************************************************************************')

    def _exec_chmod(self):
        ''' When files are write-only, tags can't be changed.
        TODO python 3 compliant: filemode 0664 is octal, -> 0o664
        ''' 
        log = logging.getLogger('%s._exec_chmod' % self.log.name)
        #self.log.debug('_exec_chmod start')
        result_rows = self.utils.changeDictsToLists(self.rows, constants.TAG_KEYS)
        changing_permissions = False
        for i, row in enumerate(result_rows):
            path = unicode(self.rows[i]['path']) # os.access wants unicode or else it thinks it's ascii, QString doesn't work
            if os.access(path, os.W_OK):
                # ok, we can write 
                pass
            else:
                #log.debug('WRITE FAILED %s +++++++++++ ' % self.rows[i]['path'])
                changing_permissions = True
                os.chmod(path, 0664)

        if changing_permissions:
            self._qtparent.blah(('*** CHANGING FILE PERMISSIONS TO WRITABLE (0664) ***', None))
        #self.log.debug('_exec_chmod end')
        return None
    
    def _saveTags(self, FOR_REAL = True):
        ''' 
        ''' 
        log = logging.getLogger('%s._saveTags' % self.log.name)
        #self.log.debug('_saveTags start')
        #for row in self.rows:
            #log.debug(row)
        self._qtparent.blah(('Writing tags', None))
        result_rows = self.utils.changeDictsToLists(self.rows, constants.TAG_KEYS)
        #self.log.debug(constants.TAG_KEYS)
        finalResult = True
        
        for i, row in enumerate(result_rows):
            if FOR_REAL:
                result = self.tagProcessor.writeFile(self.rows[i]['path'], row)
            else:
                log.debug('writing tags for %s' % self.rows[i]['path'])
                log.debug(self.rows[i])
                result = True
                
            if result == False:
                finalResult = False
                
            self._qtparent.blah(('- %s' % self.rows[i]['filename'], result))
            #self.log.debug(row)
        
        #self.log.debug('_saveTags end')
        return finalResult
    
    def _saveFileNames(self, FOR_REAL = True):
        ''' 
        ''' 
        #self.log.debug('_saveFileNames start')
        log = logging.getLogger('%s._saveFileNames' % self.log.name)
        
        self._qtparent.blah(('<br>Writing filename', None))
        result = False
        for i, row in enumerate(self.rows):
            path_string = unicode(row['path'])
            j = path_string.rfind(os.sep)
            path_string = path_string[:j]
            
            track = unicode(row['tracknumber'])
            if track.find(constants.TRACK_SEPARATOR) > -1:
                x = row['tracknumber'].find(constants.TRACK_SEPARATOR)
                if x >= 0:
                    track = row['tracknumber'][:x]
            
            track = track.replace(os.sep, constants.DISALLOWED_CHARACTER_REPLACEMENT)
            artist = row['artist'].replace(os.sep, constants.DISALLOWED_CHARACTER_REPLACEMENT)
            title = row['title'].replace(os.sep, constants.DISALLOWED_CHARACTER_REPLACEMENT)
            extension = row['extension'].replace(os.sep, constants.DISALLOWED_CHARACTER_REPLACEMENT)
            if extension[0] == '.':
                extension = extension[1:]
            
            song_string = '%s %s - %s.%s' % (track, artist, title, extension)
            song_string = song_string.strip() # remove spaces in case the tracknumber is empty
            #self.log.debug(row['path'])
            #self.log.debug(type(row['path']))
            #self.log.debug(os.path.join(path_string, song_string))
            result = True
            try:
                if FOR_REAL:
                    os.rename(unicode(row['path']), os.path.join(path_string, song_string))
                else:
                    log.debug('renaming to %s' % song_string)
                    result = True
            except Exception, e:
                self.log.error('Error renaming file name %s to %s' % (unicode(row['path']), os.path.join(path_string, song_string)))
                self.log.error(str(e))
                self.log.error(type(e))
                result = False
        
            self._qtparent.blah(('- %s  ->  %s' % (self.rows[i]['filename'], song_string), result))
        #self.log.debug('_saveFileNames end')
        return result
    
    def _saveDirectory(self, FOR_REAL = True):
        ''' 
        ''' 
        #self.log.debug('_saveDirectory start')
        self._qtparent.blah(('<br>Renaming directory', None))
        result = False
        newDirectoryName = ''
        if self.useAlbumVariousArtists:
            artist = constants.DEFAULT_ARTIST
        else:
            artist = self.albumArtist
        
        # TODO: make sure self.albumTitle is correct
        if len(self.albumTitle) == 0:
            self.log.error('no albumTitle')
            
        if len(artist) > 0:
            dir_string = '%s - %s' % (artist, self.albumTitle)
        else:
            dir_string = self.albumTitle
        
        if len(self.volumeString) > 0:
            dir_string += ' (%s)' % (self.volumeString,)
        if len(self.albumDate) > 0:
            dir_string += ' (%s)' % (self.albumDate,)
        
        #self.log.debug(dir_string)
        dir_string = dir_string.replace(os.sep, constants.DISALLOWED_CHARACTER_REPLACEMENT)
        try:
            basePath = self.fullDirectory[:self.fullDirectory.rfind(os.sep)]
            #self.log.debug('"%s" --> "%s"' % (self.fullDirectory, os.path.join(basePath, dir_string)))
            
            if FOR_REAL:
                newDirectoryName = os.path.join(basePath, dir_string)
                os.rename(self.fullDirectory, newDirectoryName)
            else:
                result = True
                newDirectoryName = self.fullDirectory
                #return True, self.fullDirectory
            result = True
            #os.rename("/home/tjalling/mp3/00test/Kognitif_My_Space_World(2012)", "/home/tjalling/mp3/00test/Kognitif - My Space World (2012)")

        except OSError, e:
            self.log.error('Error writing directory name')
            self.log.error(dir_string)
            self.log.error(e.strerror)
            self.log.error(e.errno)
            result = False
        except Exception, e:
            self.log.error('General error writing directory name')
            self.log.error(dir_string)
            self.log.error(unicode(e))
            self.log.error(type(e))
            result = False
            
        self._qtparent.blah(('- %s  ->  %s' % (self.directory, dir_string), result))
        #self.log.debug('_saveDirectory end')
        return result, newDirectoryName
    
    def _storeAlbumAttributes(self):
        ''' 
        ''' 
        #self.log.debug('_storeAlbumAttributes start')
        self.storedAlbumArtist = self.albumArtist
        self.storedAlbumTitle = self.albumTitle
        self.storedAlbumDate = self.albumDate
        #self.stored_rows = self.rows[:]
        self.fixate()
        #self.log.debug('_storeAlbumAttributes end')
        return None
    
    def reset(self):
        ''' 
        ''' 
        #self.log.debug('reset start')
        #self.albumArtist = self.storedAlbumArtist
        #self.albumTitle = self.storedAlbumTitle
        #self.albumDate = self.storedAlbumDate
        #self._setUseAlbumArtist(
        self.rows = copy.deepcopy(self.stored_rows)
        #self.log.debug('reset end')
        return None
    
    def fixate(self):
        ''' 
        ''' 
        #self.log.debug('fixate start')
        self.stored_rows = copy.deepcopy(self.rows)
        #self.log.debug('fixate end')
        return None
    
    def forceDeleteTags(self):
        ''' ''' 
        log = logging.getLogger('%s.forceDeleteTags' % self.log.name)
        #self.log.debug('forceDeleteTags start')
        self._qtparent.showSaveDialog()
        self._qtparent.blah(('Force delete', None))
        FOR_REAL = True
        #FOR_REAL = False
        for row in self.rows:
            #log.debug(row)
            if FOR_REAL:
                result = self.tagProcessor.forceDeleteTags(row['path'])
            else:
                result = True
            self._qtparent.blah(('- %s:' % row['filename'], result))
        #self.log.debug('forceDeleteTags end')
        return None
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    