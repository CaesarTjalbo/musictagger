# -*- coding: utf-8 -*-
import sys
import os

import logging

import constants

try:
    from PyQt4.QtCore import *
    qt = True
except ImportError:
    qt = False

try:
    import mutagen
    from mutagen.id3 import ID3, TIT2
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    from mutagen.mp4 import MP4
    from mutagen.oggvorbis import OggVorbis
except ImportError:
    print 'Missing dependency:'
    print 'mutagen (python-mutagen)'
    sys.exit()


class Tags(object):
    def __init__(self):
        ''' 
        ''' 
        self.log = logging.getLogger('Tags')
        #self.log.debug('__init__ start')
        
        #self.log.debug('__init__ end')
        return None
    
    def readFile(self, path):
        ''' 
        ''' 
        #self.log.debug('readFile start')
        log = logging.getLogger('%s.readFile' % self.log.name)
        is_OK = False
        
        if type(path) == unicode:
            is_OK = True
        if type(path) == str:
            path = unicode(path)
            is_OK = True
        if qt:
            if type(path) == QString:
                path = unicode(path)
                is_OK = True
        
        if is_OK:
            if os.path.exists(path):
                #log.debug('exists')
                pass
            else:
                #log.debug('not exists')
                is_OK = False
                
        # step 1: try to detect missing headers, if so create them
        # step 2: in case a FLAC doesn't contain data, try to read ID3 tags
        
        if is_OK:
            #self.log.info('here')
            result = None
            if path[-len(constants.MP3_EXTENSION):].lower() == constants.MP3_EXTENSION:
                #self.log.info
                try:
                    audio = ID3(path)
                except mutagen.id3.ID3NoHeaderError:
                    self._createID3Header(path)
                result = self._readFile_mp3(path)
                
            if path[-len(constants.FLAC_EXTENSION):].lower() == constants.FLAC_EXTENSION:
                try:
                    audio = FLAC(path)
                except mutagen.flac.FLACNoHeaderError:
                    self._createFLACHeader(path)
                result = self._readFile_flac(path)
                
                total_length = 0                                        # in case a FLAC has no FLAC tags but ID3 tags
                #log.debug('flac %s' % path)
                for tag in result:
                    total_length += len(result[tag])
                    if total_length > 0:
                        break
                
                #log.debug('total_length %d' % total_length)
                if total_length < 1:
                    mp3_result = self._readFile_mp3(path)               # in case a FLAC has no FLAC tags but ID3 tags
                    if mp3_result:
                        total_length = 0                                        # in case a FLAC has no FLAC tags but ID3 tags
                        for tag in mp3_result:
                            total_length += len(mp3_result[tag])
                        if total_length > 0:
                            log.debug('returning ID3 data')
                            return result
                            # it would seem we've got information from id3 tags.
                    else:
                        # no FLAC tags and probably no ID3 header
                        pass
            
            if path[-len(constants.MP4_EXTENSION):].lower() in constants.MP4_EXTENSION_LIST:
                self.log.debug('mp4')
                try:
                    audio = MP4(path)
                except mutagen.mp4.MP4MetadataError, e:
                    self.log.debug(type(e))
                    self.log.debug(str(e))
                    #TODO set headers for mp4
                result = self._readFile_mp4(path)
                
            if path[-len(constants.OGG_EXTENSION):].lower() == constants.OGG_EXTENSION:
                #self.log.info
                try:
                    audio = OggVorbis(path)
                except mutagen.oggvorbis.OggVorbisHeaderError:
                    self._createOggHeader(path)
                result = self._readFile_ogg(path)
        #self.log.debug('readFile end')
        return result
    
    def _readFile_mp3(self, path):
        ''' 
        ''' 
        #v2.4.0
        #COMM comment
        #TALB album
        #TDRL release time
        #TIT1 Content group description
        #TIT2 Title/songname/content description
        #TIT3 Subtitle/Description refinement
        #TOAL Original album/movie/show title
        #TOFN Original filename
        #TPE1 Lead performer(s)/Soloist(s)
        #TPE2 Band/orchestra/accompaniment
        #TPE3 Conductor/performer refinement
        #TPE4 Interpreted, remixed, or otherwise modified by
        #TPOS Part of a set
        #TRCK Track number/Position in set
        
        #v2.3
        #COMM Comments
        #TALB Album/Movie/Show title
        #TDAT Date
        #TIT1 Content group description
        #TIT2 Title/songname/content description
        #TIT3 Subtitle/Description refinement
        #TOAL Original album/movie/show title
        #TOFN Original filename
        #TOLY Original lyricist(s)/text writer(s)
        #TOPE Original artist(s)/performer(s)
        #TORY Original release year
        #TPE1 Lead performer(s)/Soloist(s)
        #TPE2 Band/orchestra/accompaniment
        #TPE3 Conductor/performer refinement
        #TPE4 Interpreted, remixed, or otherwise modified by
        #TPOS Part of a set
        #TRCK Track number/Position in set
        #TYER Year

        #Title – The track title
        #Artist – The artist that recorded the track
        #Album – Which album the track belongs to (if applicable
        #Track – The track number from the album (if applicable)
        #Year – The year that the track was published
        #Genre – The type of track, e.g. speech, rock, pop
        #Comment – Additional notes about the track
        #Copyright – Copyright notice by the copyright holder
        #Album Art – Thumbnail of the album art or artist        

        #self.log.debug('_readFile_mp3 start')
        log = logging.getLogger('%s._readFile_mp3' % self.log.name)
        try:
            audio = ID3(path)
        except mutagen.id3.ID3BadUnsynchData, e:
            log.error(type(e))
            log.error('Mutagen error parsing id3 data for:')
            log.error(path)
            return None
        except mutagen.id3.ID3NoHeaderError, e:
            # because we use this method for FLAC too but a FLAC doesn't have to have an ID3 header and that's ok
            if path[-len(constants.FLAC_EXTENSION): ] == constants.FLAC_EXTENSION:
                return None
            log.error(type(e))
            log.error('Mutagen error parsing id3 data for:')
            log.error(path)
                #self._createID3Header(path)
            #return None
        
        result = dict()
        for i, tag in enumerate(constants.MP3TAGS):
            try:
                if tag == 'COMM':
                    # mostly, the COMM tag isn't present and will eventually give a KeyError, which allows us to set a default value
                    # when there's a COMM tag, it's not just "COMM" but has a greater length. Examples:
                    # "COMM::'\x00\x00\x00'"
                    # "COMM:iTunNORM:'eng'"
                    commKey = None 
                    for t in audio.keys():
                        if t[:4] == 'COMM':
                            commKey = t
                            #log.debug(commKey)
                            break
                    if commKey:
                        tag = commKey
                    else:
                        tag = 'COMM'

                if type(audio[tag]) == list: # we might get a list of tags, in that case use the only item or return the list
                    if len(audio[tag]) == 1:
                        result[constants.TAG_KEYS[i]] = unicode(audio[tag][0])
                    else:
                        result[constants.TAG_KEYS[i]] = unicode(audio[tag])
                else:
                        result[constants.TAG_KEYS[i]] = unicode(audio[tag])
            except KeyError, e:
                result[constants.TAG_KEYS[i]] = unicode('')
        #log.debug(result)
        
        #self.log.debug('_readFile_mp3 end')
        return result
    
    
    def _readFile_flac(self, path):
        ''' 
        ''' 
        #TITLE Track/Work name
        #ALBUM The collection name to which this track belongs
        #TRACKNUMBER The track number of this piece if part of a specific larger collection or album
        #ARTIST The artist generally considered responsible for the work. In popular music this is usually the performing band or singer. For classical music it would be the composer. For an audio book it would be the author of the original text.
        #PERFORMER The artist(s) who performed the work. In classical music this would be the conductor, orchestra, soloists. In an audio book it would be the actor who did the reading. In popular music this is typically the same as the ARTIST and is omitted.
        #DESCRIPTION A short text description of the contents
        #DATE Date the track was recorded
        
        #self.log.debug('_readFile_flac start')
        audio = FLAC(path)
        result = dict()
        log = logging.getLogger('%s._readFile_flac' % self.log.name)
        #for i, tag in enumerate(constants.FLACTAGS):
        for i, tag in enumerate(constants.TAG_KEYS):
            try:
                if type(audio[tag]) == list: # we might get a list of tags, in that case use the only item or return the list
                    if len(audio[tag]) == 1:
                        result[constants.TAG_KEYS[i]] = unicode(audio[tag][0])
                    else:
                        result[constants.TAG_KEYS[i]] = unicode(audio[tag])
                else:
                    result[constants.TAG_KEYS[i]] = unicode(audio[tag])
            except KeyError:
                result[constants.TAG_KEYS[i]] = unicode('')
        #log.debug(audio.keys())
        #self.log.debug('_readFile_flac end')
        return result
    
    def _readFile_mp4(self, path):
        ''' ''' 
        log = logging.getLogger('%s._readFile_mp4' % self.log.name)
        #self.log.debug('_readFile_mp4 start')
        try:
            audio = MP4(path)
        except Exception, e:
            log.debug(type(e))
            log.debug(str(e))
        
        result = dict()
        for i, tag in enumerate(constants.MP4TAGS):
            try:
                if tag == 'trkn':
                    result[constants.TAG_KEYS[i]] = audio.tags[tag][0][0]
                else:
                    if type(audio.tags[tag]) == list:
                        if len(audio.tags[tag]) == 1:
                            result[constants.TAG_KEYS[i]] = unicode(audio.tags[tag][0])
                        else:
                            result[constants.TAG_KEYS[i]] = unicode(audio.tags[tag])
                    else:
                        result[constants.TAG_KEYS[i]] = unicode(audio.tags[tag])
            except KeyError, e:
                log.debug('tag "%s" is missing' % tag)
                log.debug(type(e))
                log.debug(str(e))
                result[constants.TAG_KEYS[i]] = u''
                
            except Exception, e:
                log.debug(type(e))
                log.debug(str(e))
                result[constants.TAG_KEYS[i]] = u''
            
        log.debug(dir(audio))
        for key in audio.tags.keys():
            if key in constants.MP4TAGS:
                log.debug(key)
                log.debug(audio.tags[key])
        
        #self.log.debug('_readFile_mp4 end')
        return result
    
    def _readFile_ogg(self, path):
        ''' ''' 
        log = logging.getLogger('%s._readFile_ogg' % self.log.name)
        self.log.debug('_readFile_ogg start')
        try:
            audio = OggVorbis(path)
        except Exception, e:
            log.debug(type(e))
            log.debug(str(e))
        
        result = dict()
        
        for i, tag in enumerate(constants.OGGTAGS):
            try:
                if type(audio.tags[tag]) == list:
                    if len(audio.tags[tag]) == 1:
                        result[constants.TAG_KEYS[i]] = unicode(audio.tags[tag][0])
                    else:
                        result[constants.TAG_KEYS[i]] = unicode(audio.tags[tag])
                else:
                    result[constants.TAG_KEYS[i]] = unicode(audio.tags[tag])
            except KeyError, e:
                #log.debug('tag "%s" is missing' % tag)
                #log.debug(type(e))
                #log.debug(str(e))
                result[constants.TAG_KEYS[i]] = u''
            except Exception, e:
                log.debug(type(e))
                log.debug(str(e))
            
        #self.log.debug('_readFile_ogg end')
        return result
    
    
    def writeFile(self, path, values):
        ''' 
        ''' 
        #self.log.debug('writeFile start')
        log = logging.getLogger('%s.writeFile' % self.log.name)
        is_OK = False
        
        if type(path) == unicode:
            is_OK = True
        if type(path) == str:
            path = unicode(path)
            is_OK = True
        if qt:
            if type(path) == QString:
                path = unicode(path)
                is_OK = True
        
        if is_OK:
            if os.path.exists(path):
                #log.debug('exists')
                pass
            else:
                #log.debug('not exists')
                is_OK = False
        
        success = False
        if is_OK:
            if path[-len(constants.MP3_EXTENSION):].lower() == constants.MP3_EXTENSION:
                success = self._writeFile_mp3(path, values)
            if path[-len(constants.FLAC_EXTENSION):].lower() == constants.FLAC_EXTENSION:
                success = self._writeFile_flac(path, values)
            if path[-len(constants.MP4_EXTENSION):].lower() in constants.MP4_EXTENSION_LIST:
                success = self._writeFile_mp4(path, values)
            if path[-len(constants.OGG_EXTENSION):].lower() == constants.OGG_EXTENSION:
                success = self._writeFile_ogg(path, values)
        
        #self.log.debug('writeFile end')
        return success
    
    def _writeFile_mp3(self, path, values):
        ''' 
        ''' 
        #self.log.debug('_writeFile_mp3 start')
        log = logging.getLogger('%s._writeFile_mp3' % self.log.name)
        success = False
        try:
            audio = ID3(path)
            success = True
        except mutagen.id3.ID3BadUnsynchData, e:
            #success = False
            log.error(type(e))
            log.error('Mutagen error parsing id3 data for:')
            log.error(path)
            return False
        except mutagen.id3.ID3NoHeaderError, e:
            #success = False
            log.error(type(e))
            log.error('Mutagen error parsing id3 data for:')
            log.error(path)
            return False
        except Exception, e:
            #success = False
            log.error('General exception')
            log.error(type(e))
            log.error(unicode(e))
            #log.error('Mutagen error parsing id3 data for:')
            log.error(path)
            return False
            
        #log.debug(dir(audio))
        if success:
            for i, key in enumerate(constants.MP3TAGS):
                try:
                    #log.debug('"%s" = "%s"' % (key, values[i]))
                    #TODO: code breaks when a list is given
                    if key == 'COMM':
                        # check if there's more than 1 COMM field
                        # the problem is that an exsisting COMM field might show up before the field being set here
                        # in that case the new COMM field won't show up.
                        try:
                            ###a = audio.getall('COMM')
                            ###if len(a) > 1:
                                ###log.debug('trying to delete COMM')
                            audio.delall('COMM')
                                #set them all to empty strings
                                #try:
                                    #dummy = mutagen.id3.COMM
                                    #dummy.text = u''
                                    #dummy.encoding = 3
                                    #v = [dummy for x in range(len(a))]
                                    #audio.setall('COMM', v)
                                #except Exception, e:
                                    #log.debug('trying audio.Setall(\'COMM\')')
                                    #log.error(type(e))
                                    #log.error(str(e))
                        except Exception, e:
                            log.debug('trying audio.delall(\'COMM\')')
                            log.error(type(e))
                            log.error(str(e))
                            
                        #log.info(values[i])
                        values[i] = values[i].replace('"', '\\\"')
                        #log.info(values[i])
                        s = 'mutagen.id3.%s(encoding = 3, lang = "eng", desc = "", text="%s")' % (key, values[i])
                    else:
                        values[i] = values[i].replace('"', '\\\"')
                        s = 'mutagen.id3.%s(encoding = 3, text=u"%s")' % (key, values[i])
                    #log.debug(s)
                    o = eval(s)
                    audio.add(o)
                    success = True
                except ValueError, e:
                    log.debug('ValueError: %s' % str(e))
                    success = False
                except Exception, e:
                    log.error('Error setting mp3 tag %s with value "%s" for file %s' % (key, values[i], path))
                    log.error(type(e))
                    log.error(str(e))
                    success = False
        else:
            log.debug('HERE')

        
        try:
            audio.save()
            success = True
            #pass
        except Exception, e:
            log.error('Error saving tags for file %s' % (path, ))
            log.error(type(e))
            log.error(str(e))
            success = False
            
            
            
        #self.log.debug('_writeFile_mp3 end')
        return success
    
    def _writeFile_flac(self, path, values):
        ''' 
        ''' 
        #self.log.debug('_writeFile_flac start')
        log = logging.getLogger('%s._writeFile_flac' % self.log.name)
        success = False
        try:
            # if there are ID3 tags in the FLAC, attempt to remove them
            audio = ID3(path)
            log.info('found ID3 tags in FLAC')
            audio.delete()
        except mutagen.id3.ID3NoHeaderError:
            pass
        except Exception, e:
            log.error('General exception trying for ID3 in FLAC file')
            log.error(type(e))
            log.error(unicode(e))
            log.error(path)
            log.error('EVER REACHED?')
        
        try:
            audio = FLAC(path)
            success = True
        except Exception, e:
            #success = False
            log.error('General exception accessing FLAC file')
            log.error(type(e))
            log.error(unicode(e))
            log.error(path)
            log.error('EVER REACHED?')
            success = False
        
        if success:
            for i, key in enumerate(constants.FLACTAGS):
                try:
                    audio[key] = values[i]
                    #log.debug('flac: key = "%s", value = "%s"' % (key, values[i]))
                    success = True
                except Exception, e:
                    log.error('Error setting flac tag %s with value "%s" for file %s' % (key, values[i], path))
                    log.error(type(e))
                    log.error(str(e))
                    log.error('EVER REACHED?')
                    success = False
        if success:
            try:
                audio.save()
                success = True
                pass
            except Exception, e:
                log.error('Error saving tags for file %s' % (path, ))
                log.error(type(e))
                log.error(str(e))
                log.error('EVER REACHED?')
                success = False
            
        #self.log.debug('_writeFile_flac end')
        return success

    def _writeFile_mp4(self, path, values):
        ''' ''' 
        log = logging.getLogger('%s._writeFile_mp4' % self.log.name)
        #self.log.debug('_writeFile_mp4 start')
        success = False
        try:
            audio = MP4(path)
            success = True
        except Exception, e:
            #success = False
            log.error('General exception accessing MP4 file')
            log.error(type(e))
            log.error(unicode(e))
            log.error(path)
            success = False
            
        #log.debug('success = %s' % success)
        if success:
            #log.debug('writing tags for %s' % path)
            #log.debug(values)
            for i, key in enumerate(constants.MP4TAGS):
                #raise NotImplementedError
                try:
                    total_tracks = 0
                    if key == 'trkn':
                        audio.tags[key] = [(int(values[i]), total_tracks)]
                    else:
                        audio.tags[key] = [values[i]]
                except Exception, e:
                    log.error(type(e))
                    log.error(unicode(e))
                    log.error(path)
                    log.error('EVER REACHED?')
                    
            try:
                audio.save()
                success = True
                pass
            except Exception, e:
                log.error('Error saving tags for file %s' % (path, ))
                log.error(type(e))
                log.error(str(e))
                log.error('EVER REACHED?')
                success = False
        #self.log.debug('_writeFile_mp4 end')
        return success
    
    def _writeFile_ogg(self, path, values):
        ''' ''' 
        log = logging.getLogger('%s._writeFile_ogg' % self.log.name)
        self.log.debug('_writeFile_ogg start')
        
        success = False
        try:
            audio = OggVorbis(path)
            success = True
        except Exception, e:
            log.error('Error saving tags for file %s' % (path, ))
            log.error(type(e))
            log.error(str(e))
            log.error('EVER REACHED?')
            success = False
        
        if success:
            for i, key in enumerate(constants.OGGTAGS):
                audio.tags[key] = [values[i]]
        if success:
            try:
                audio.save()
                success = True
                pass
            except Exception, e:
                log.error('Error saving tags for file %s' % (path, ))
                log.error(type(e))
                log.error(str(e))
                log.error('EVER REACHED?')
                success = False
        #self.log.debug('_writeFile_ogg end')
        return success
    
    def createHeader(self):
        ''' 
        ''' 
        log = logging.getLogger('%s.createHeader' % self.log.name)
        #self.log.debug('createHeader start')
        if path[-len(constants.MP3_EXTENSION):].lower() == constants.MP3_EXTENSION:
            result = self._createID3Header(path)
        if path[-len(constants.FLAC_EXTENSION):].lower() == constants.FLAC_EXTENSION:
            result = self._createFLACHeader(path)
            
        
        #self.log.debug('createHeader end')
        return None
    
    
    def _createID3Header(self, path):
        ''' ''' 
        log = logging.getLogger('%s._createID3Header' % self.log.name)
        self.log.debug('_createID3Header start')
        audio = MP3(path)
        audio['TIT2'] = TIT2(encoding=3, text=[''])
        audio.save()
        #self.log.debug('_createID3Header end')
        return None
    
    def _createFLACHeader(self, path):
        ''' ''' 
        log = logging.getLogger('%s._createFLACHeader' % self.log.name)
        self.log.debug('_createFLACHeader start')
        audio = mutagen.flac.FLAC(path)
        audio['TITLE'] = u''
        audio.save()
        
        #self.log.debug('_createFLACHeader end')
        return None
    
    def _createOggHeader(self):
        ''' ''' 
        #log = logging.getLogger('%s._createOggHeader' % self.log.name)
        self.log.debug('_createOggHeader start')
        
        #self.log.debug('_createOggHeader end')
        return None
    
    def forceDeleteTags(self, path):
        ''' ''' 
        log = logging.getLogger('%s.forceDeleteTags' % self.log.name)
        #self.log.debug('forceDeleteTags start')
        
        result = False
        
        path = unicode(path)
        extension_index = path.rfind('.')
        if extension_index > 0:
            try:
                extension = path[extension_index + 1:]
                if extension.lower() == constants.MP3_EXTENSION:
                    #log.debug('MP3: %s' % path)
                    audio = ID3(path)
                    audio.delete(path, True, True)
                    result = True
                if extension.lower() == constants.FLAC_EXTENSION:
                    #log.debug('FLAC: %s' % path)
                    audio = FLAC(path)
                    audio.delete()
                    result = True
                if extension.lower() in constants.MP4_EXTENSION_LIST:
                    #log.debug('MP4: %s' % path)
                    mutagen.mp4.delete(path)
                    result = True
            except Exception, e:
                log.debug(type(e))
                log.debug(str(e))
                result = False
        else:
            pass
            
        #self.log.debug('forceDeleteTags end')
        return result
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    