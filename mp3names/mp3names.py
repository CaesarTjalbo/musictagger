#!/usr/bin/env python
############################################################################
#    Copyright (C) 2007 by tjalling,,,   #
#    tjalling@siduxbox   #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

# file: mp3names.py

import sys
import os

sys.path.insert(0, os.path.join(sys.path[0], 'ui_files'))

import logging
import argparse

import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import mainwindow

import rules_module
import rules1
import utils_module
import test_encodings

def main(argv):
    '''
    '''
    ## BEGIN logging and commandline options
    log = logging.getLogger('')
    handler = logging.StreamHandler()
    fmt = '%H:%M:%S'
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', fmt)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    #log.setLevel(logging.INFO)
    #log.setLevel(logging.CRITICAL)
    #log.debug('started')

    p = argparse.ArgumentParser()
    p.add_argument('--verbose', '-v', default = False,action = 'store_true', help = 'outputs debugging information')
    arguments = p.parse_args()

    ## END logging and commandline options
    
    test = True
    test = False
    
    if test:
        #test_encodings.pipo()
        #r = rules_module.Rules()
        u = utils_module.Utils()
        words = [123, 'ABCD', u'..ABCD', u'ABCD..', u'..ABCD..', u'..AB..CD..', u'....', u'[]{}()']
        title = "It's Gonna Be A Mess (Pt. Ii)"
        #words = title.split()
        for word in words:
            print word
            print rules1.strip_punctuation(word)
            print
        
        l = logging.getLogger('lognaam')
        l.debug(dir(l))
        l.debug(l.name)
        #r.setup()
    else:
        start()


def start():
    app = QApplication(sys.argv)
    form = mainwindow.MainWindow()

    form.setupUi(form)
    form.setup()
    form.show()
    app.exec_()
    return None
            
            
            
            
            
            
            
if __name__ == '__main__':
    main(sys.argv)


''' TODO
- clean text from free



'''











