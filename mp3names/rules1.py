# -*- coding: utf-8 -*-
import sys
import os
import logging
import random

import string
import re
import constants

    
class AbstractRule(object):
    ''' '''
    displayName = '' # name displayed on screen
    rank = -1 # order in which the rules are displayed
    name = '' # same as class name
    toolTip = '' # 
    initially_checked = True 
    checked = initially_checked
    needsInput = False # to set a lineEdit under the rule
    allRows = False # when it needs all the rows as input, typically for numbering
    keys = ['tracknumber', 'artist', 'title', 'date', 'album', 'comment'] # all the tags the rule should work on
    
    def __init__(self):
        ''' 
        ''' 
        self.log = logging.getLogger(self.name)
        #self.log.debug('__init__ start')
        
        #self.log.debug('__init__ end')
        return None
    
    def execute(self, param):
        ''' 
        ''' 
        #self.log.debug('execute start')
        if type(param) is unicode or type(param) is str:
            param = self._executeOnString(param)
        if type(param) is dict:
            param = self._executeOnDict(param)
        #self.log.debug('execute end')
        return param

    def setRows(self, rows):
        ''' 
        ''' 
        #self.log.debug('setRows start')
        self.rows = rows
        #self.log.debug('setRows end')
        return None
    
    def _executeOnString(self, param):
        ''' 
        ''' 
        #self.log.debug('_executeOnString start')
        raise NotImplementedError
        #self.log.debug('_executeOnString end')
        return param
    
    def _executeOnDict(self, param):
        ''' 
        ''' 
        #self.log.debug('_executeOnDict start')
        for key in param:
            if key in self.keys:
                if type(param[key]) is unicode or type(param[key]) is str:
                    param[key] = self._executeOnString(param[key])
                #apparently m4a can have tracknumber as an int
                elif type(param[key]) is int:
                    param[key] = self._executeOnString(str(param[key]))
                else:
                    self.log.debug('dict, param[%s] != str, unicode or int but is %s' % (key, type(param[key])))
        #self.log.debug('_executeOnDict end')
        return param
    
class Rule_Strip(AbstractRule):
    ''' '''
    displayName = 'Strip white space'
    rank = 10
    name = 'Rule_Strip'
    toolTip = 'Strips leading and trailing whitespace.'
    initially_checked = True
    
    def _executeOnString(self, param):
        return param.strip()
        
class Rule_ChangeQuotes(AbstractRule):
    ''' '''
    displayName = 'Change quotes'
    rank = 20
    name = 'Rule_ChangeQuotes'
    toolTip = 'Change funny quotes for standard quotes.'
    initially_checked = True
    
    def _executeOnString(self, param):
        ''' 
        ''' 
        log = logging.getLogger('%s.Rule_ChangeQuotes._executeOnString' % self.log.name)
        #self.log.debug('_executeOnString start')
        single = [u'‘', u'’', u'‚', u'‛', u'❛', u'❜', u'❟', u'′', u'´', u'']
        double = [u'❝', u'❞', u'❠', u'“', u'”', u'„', u'‟', u'〝', u'〞', u'〟', u'＂']
        
        #if param.lower()[:6] == 'rocket':
            #log.debug(param)
            #for c in param:
                #log.debug(
        try:
            for c in single:
                param = param.replace(c, u'\'')
        except UnicodeDecodeError, ude:
            #log.debug('UnicodeDecodeError')
            #log.debug(str(ude))
            #log.debug(param)
            pass
            
        try:
            for c in double:
                param = param.replace(c, u'"')
        except UnicodeDecodeError, ude:
            #log.debug('UnicodeDecodeError')
            #log.debug(str(ude))
            #log.debug(param)
            pass
        #for i, c in enumerate(param):
            #if c in single:
                #log.debug(ord(c))
                #param[i] = unicode(chr(27))
            #if c in double:
                #log.debug(ord(c))
                #param[i] = u'"'
        #self.log.debug('_executeOnString end')
        return param

class Rule_Capitalize(AbstractRule):
    displayName = 'Capitalize'
    rank = 40
    name = 'Rule_Capitalize'
    toolTip = 'Capitalize every word.'
    #checked = True
    #initially_checked = True
    #needsInput = False

    def _executeOnString(self, param):
        ''' 
        ''' 
        #self.log.debug('_executeOnString start')
        #self.log.debug(param)
        l = param.split()
        for i, s in enumerate(l):
            if len(s) > 0:
                if s[0] in string.ascii_letters:
                    l[i] = s.capitalize()
                else:
                    if s[0] in string.punctuation:
                        j = 0
                        for j in range(len(s)):
                            if s[j] in string.punctuation:
                                pass
                            else:
                                break
                        l[i] = s[:j] + s[j].upper() + s[j + 1:].lower()
            #self.log.debug(l[i])
        param = ' '.join(l)
        #self.log.debug(param)
        #self.log.debug('_executeOnString end')
        return param
    
class Rule_ReCapitalizeNames(AbstractRule):
    displayName = 'Capitalize Names'
    rank = 41
    name = 'Rule_ReCapitalizeNames'
    toolTip = 'Correct names like O\'Jays and McDonald.'
    #checked = True
    #initially_checked = True
    #needsInput = False

    def _executeOnString(self, param):
        ''' 
        ''' 
        #self.log.debug('_executeOnString start')
        #self.log.debug(param)
        l = param.split()
        for i, s in enumerate(l):
            if len(s) > 2:
                if s[0:2].lower() == 'mc':
                    #McDonalds
                    l[i] = 'Mc' + s[2].upper() + s[3:]
                if s[0:2].lower() == "o'":
                    # O'Jays
                    l[i] = "O'" + s[2].upper() + s[3:]
                #if s[1] == "'" and s[0].lower() != 'i' and s[0].lower() in string.lowercase:
                    ## O'Jays, L'Oreal but not I'M, I'Ve ..... ow ow  C'Est 
                    #l[i] = '%s\'%s%s' % (s[0].upper(), s[2].upper(), s[3:])
            #self.log.debug(l[i])
        param = ' '.join(l)
        #self.log.debug(param)
        #self.log.debug('_executeOnString end')
        return param
    
class Rule_ReCapitalizeAbbreviations(AbstractRule):
    displayName = 'Capitalize Abbreviations'
    rank = 41
    name = 'Rule_ReCapitalizeAbbreviations'
    toolTip = 'Correct abbreviations.'
    #checked = True
    #initially_checked = True
    #needsInput = False

    def _executeOnString(self, param):
        ''' 
        ''' 
        #self.log.debug('_executeOnString start')
        #self.log.debug(param)
        l = param.split()
        for i, s in enumerate(l):
            if s.count('.') > 1:
                l2 = s.split('.')
                l3 = [t.capitalize() for t in l2]
                l[i] = '.'.join(l3)
                    
            #self.log.debug(l[i])
        param = ' '.join(l)
        #self.log.debug(param)
        #self.log.debug('_executeOnString end')
        return param
    
class Rule_RemoveUnderscores(AbstractRule):
    displayName = 'Remove underscores'
    rank = 30
    name = 'Rule_RemoveUnderscores'
    toolTip = 'Remove underscores from words and replace them with spaces.'
    initially_checked = False
        
    def _executeOnString(self, param):
        ''' 
        ''' 
        #self.log.debug('_executeOnString start')
        
        #self.log.debug('_executeOnString end')
        return param.replace('_', ' ')

    
class Rule_FillTrackNumber(AbstractRule):
    ''' '''
    displayName = 'Fill track number'
    rank = 60
    name = 'Rule_FillTrackNumber'
    toolTip = 'Fill track number with zeroes so every track number is of equal length.'
    initially_checked = True
    allRows = True
    keys = ['tracknumber']

    def execute(self, param):
        ''' 
        ''' 
        #log = logging.getLogger('Rule_FillTrackNumber')
        #log.debug('execute start')
        #if type(param) is unicode or type(param) is str:
            #param = self._executeOnString(param)
        if type(param) is dict:
            param = self._executeOnDict(param)
        #self.log.debug('execute end')
        return param

    def _executeOnString(self, param):
        ''' 
        ''' 
        #self.log.debug('_executeOnString start')
        s = '%%0%dd' % len(str(len(self.rows)))
        if param.find(constants.TRACK_SEPARATOR) >= 0:
            i = param.index(constants.TRACK_SEPARATOR)
            number = param[:i]
            restPart = param[i:]
        else:
            number = param
            restPart = ''
        
        try:
            number = int(number)
        except ValueError:
            return param
        
        firstPart = s % number
        return '%s%s' % (firstPart, restPart)
        #self.log.debug('_executeOnString end')
        return param
    
class Rule_PadTrackNumber(AbstractRule):
    ''' '''
    displayName = 'Pad track number'
    rank = 70
    name = 'Rule_PadTrackNumber'
    toolTip = 'Add a leading zero if the track number consists of 1 digit.'
    initially_checked = True
    keys = ['tracknumber']
    
    def execute(self, param):
        ''' 
        ''' 
        #self.log.debug('execute start')
        #if type(param) is unicode or type(param) is str:
            #param = self._executeOnString(param)
        
        # need to control on what it works so we can't accept input on string
        #self.log.debug('type param %s' % type(param))
        if type(param) is dict:
            param = self._executeOnDict(param)
        #self.log.debug('execute end')
        return param

    def _executeOnString(self, param):
        ''' 
        ''' 
        #self.log.debug('_executeOnString start')
        if param.find(constants.TRACK_SEPARATOR) >= 0:
            #self.log.debug('here')
            i = param.index(constants.TRACK_SEPARATOR)
            firstPart = param[:i]
            restPart = param[i:]
        else:
            #self.log.debug('there')
            firstPart = param
            restPart = ''
        #self.log.debug('type tracknumber %s' % type(firstPart))
        if len(firstPart) == 1:
            firstPart = '0%s' % firstPart
            
        return '%s%s' % (firstPart, restPart)
        #self.log.debug('_executeOnString end')
        return param
    
class Rule_RemoveString(AbstractRule):
    ''' '''
    displayName = 'Remove string'
    rank = 170
    name = 'Rule_RemoveString'
    toolTip = 'Select this rule and enter characters to remove from words.'
    initially_checked = False
    needsInput = True
    
    def _executeOnString(self, param):
        ''' 
        ''' 
        #self.log.debug('_executeOnString start')
        #self.log.debug(param)
        #if self.inputWidget:
            #if hasattr(self.inputWidget, 'text'):
                #t = unicode(self.inputWidget.text())
                #if len(t) > 0:
        try:
            t = unicode(self.inputWidget.text())
            c = param.count(t)
            for i in range(c):
                j = param.index(t)
                param = param[:j] + param[j + len(t):]
        except ValueError:
            pass 
            # inputWidget.text() not found in param
        except AttributeError, e:
            self.log.debug(type(e))
            self.log.debug(str(e))
            pass
            # no inputWidget
            # no inputWidget.text()
        except Exception, e:
            self.log.debug(type(e))
            self.log.debug(str(e))
            pass 
            # no conversion inputWidget.text() to unicode
            # whatever
       
        #self.log.debug('_executeOnString end')
        return param
    
class Rule_SwapArtistTitle(AbstractRule):
    ''' '''
    displayName = 'Swap artist and title'
    rank = 200
    name = 'Rule_SwapArtistTitle'
    toolTip = 'Turn artist into song title and vice versa.'
    initially_checked = False
    checked = initially_checked
    executeOnce = True

    def execute(self, param):
        ''' 
        ''' 
        #self.log.debug('execute start')
        if type(param) is dict:
            param = self._executeOnDict(param)
        #self.log.debug('execute end')
        return param

    def _executeOnDict(self, param):
        ''' 
        ''' 
        #self.log.debug('_executeOnDict start')
        if 'artist' in param.keys() and 'title' in param.keys():
            param['artist'], param['title'] = param['title'], param['artist']
        #self.log.debug('_executeOnDict end')
        return param

class Rule_RemoveTotalTrackNumber(AbstractRule):
    ''' '''
    displayName = 'Remove the tracknumber total'
    rank = 80
    name = 'Rule_RemoveTotalTrackNumber'
    toolTip = 'If the tracknumber contains a slash and the total amount of tracks, remove this information.'
    initially_checked = True
    keys = ['tracknumber']
    
    def execute(self, param):
        ''' 
        ''' 
        #self.log.debug('execute start')
        #if type(param) is unicode or type(param) is str:
            #param = self._executeOnString(param)
        
        # need to control on what it works so we can't accept input on string
        if type(param) is dict:
            param = self._executeOnDict(param)
        #self.log.debug('execute end')
        return param

    def _executeOnString(self, param):
        ''' 
        ''' 
        #self.log.debug('_executeOnString start')
        if param.find(constants.TRACK_SEPARATOR) >= 0:
            return param[ :param.index(constants.TRACK_SEPARATOR)]
        #self.log.debug('_executeOnString end')
        return param

class Rule_RomanNumbersAllUpperCase(AbstractRule):
    displayName = 'Roman numbers in upper case'
    rank = 100
    name = 'Rule_RomanNumbersAllUpperCase'
    toolTip = 'Make all roman numbers in upper case.'
    initially_checked = True
    keys = ['artist', 'title', 'album', 'comment'] # all the tags the rule should work on
    log = logging.getLogger('Rule_RomanNumbersAllUpperCase')
    
    roman_characters = ('i', 'v', 'x', 'l', 'c', 'd', 'm')
    
    def _executeOnString(self, param):
        ''' ''' 
        #self.log.debug('_executeOnString start')
        words = param.split()
        alt_words = words[:]
        #self.log.debug(alt_words)
        for i, word in enumerate(words):
            if len(word) <= 1:
                pass
            else:
            
                success = True
                left_punctuation, word, right_punctuation = strip_punctuation(word)
                #self.log.debug('"%s", "%s", "%s"' % (left_punctuation, word, right_punctuation))
                #word = word.strip(string.punctuation)
                for c in word.lower():
                    if c in self.roman_characters:
                        pass
                    else:
                        success = False
                        word = ''.join([left_punctuation, word, right_punctuation])
                        break
                        
                if success:
                    #self.log.debug('*******%s*******' % word)
                    pattern = '''
                                ^                   # beginning of string
                                M{0,4}              # thousands - 0 to 4 M's
                                (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                                                    #            or 500-800 (D, followed by 0 to 3 C's)
                                (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                                                    #        or 50-80 (L, followed by 0 to 3 X's)
                                (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                                                    #        or 5-8 (V, followed by 0 to 3 I's)
                                $                   # end of string
                                '''
                    if re.search(pattern, word.upper(), re.VERBOSE):
                        alt_words[i] = ''.join([left_punctuation, word.upper(), right_punctuation])
            param = ' '.join(alt_words)
        #self.log.debug('_executeOnString end')
        return param


def strip_punctuation(word):
    '''return tuple with punctuation, word, punctuation ''' 
    #log = logging.getLogger('%s.strip_punctuation' % self.log.name)
    #self.log.debug('strip_punctuation start')
    left_punctuation = ''
    right_punctuation = ''
    
    if type(word) == str or type(word) == unicode:
        i = len(word) - len(word.lstrip(string.punctuation))
        left_punctuation = word[:i]
        word = word[i:]
        
        i = len(word) - len(word.rstrip(string.punctuation))
        right_punctuation = word[len(word) - i:]
        word = word[:len(word) - i]
    #self.log.debug('strip_punctuation end')
    return (left_punctuation, word, right_punctuation)


#class Removed___Rule_RemoveOSCharacters(AbstractRule):
    #displayName = 'Remove OS characters' # name displayed on screen
    #rank = 3 # order in which the rules are displayed
    #name = 'Rule_RemoveOSCharacters' # same as class name
    #toolTip = 'Remove / and replace with %s.' % constants.DISALLOWED_CHARACTER_REPLACEMENT# 
    #initially_checked = True 
    
    #def execute(self, param):
        #''' 
        #''' 
        ##self.log.debug('execute start')
        ##if type(param) is unicode or type(param) is str:
            ##param = self._executeOnString(param)
        #if type(param) is dict:
            #param = self._executeOnDict(param)
        ##self.log.debug('execute end')
        #return param

    #def _executeOnString(self, param):
        #''' 
        #''' 
        ##self.log.debug('_executeOnString start')
        #param = param.replace(os.sep, constants.DISALLOWED_CHARACTER_REPLACEMENT)
        
        ## because we might not want it at the end:
        #if param[-len(constants.DISALLOWED_CHARACTER_REPLACEMENT): ] == constants.DISALLOWED_CHARACTER_REPLACEMENT:
            #param = param[:-len(constants.DISALLOWED_CHARACTER_REPLACEMENT)]
        ##self.log.debug('_executeOnString end')
        #return param
    
    #def _executeOnDict(self, param):
        #''' 
        #''' 
        ##self.log.debug('_executeOnDict start')
        #keys = ['tracknumber', 'artist', 'title', 'extension', 'album']
        #for key in param:
            #if key in keys:
                #if type(param[key]) is unicode or type(param[key]) is str:
                    #param[key] = self._executeOnString(param[key])
        ##self.log.debug('_executeOnDict end')
        #return param




































































    