# -*- coding: utf-8 -*-
import sys
import os
import logging
import random

from functools import partial

import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#import PyKDE4
#from PyKDE4.kdecore import *
#from PyKDE4.kdeui import *

#import album_module
import config
import constants

import dialog_saved

class SaveDialog(QDialog, dialog_saved.Ui_DialogSaved):
    def __init__(self, parent):
        ''' ''' 
        #log = logging.getLogger('%s.__init__' % self.log.name)
        self.log = logging.getLogger('SaveDialog')
        #self.log.debug('__init__ start')
        super(SaveDialog, self).__init__(parent)
        #self.log.debug('__init__ end')
        return None
    
    