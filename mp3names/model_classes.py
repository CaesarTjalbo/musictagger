# -*- coding: utf-8 -*-
import sys
import os
import logging
import random

import PyQt4
from PyQt4.QtCore import *
#from PyQt4.QtCore import QAbstractTableModel

import constants


class Model(QAbstractTableModel):
    keys = list()
    modelType = None
    
    def __init__(self, parent = None):
        ''' ''' 
        self.log = logging.getLogger('Model')
        #self.log.debug('__init__ start')
        super(QAbstractTableModel, self).__init__(parent)

    def rowCount(self, parent = None):
        ''' ''' 
        #self.log.debug('rowCount start')
        #self.log.debug('rowCount end')
        if hasattr(self, 'album') and self.album:
            if hasattr(self.album, 'rows'):
                return len(self.album.rows)
        return 0
    
    def columnCount(self, parent = None):
        ''' ''' 
        #self.log.debug('columnCount start')
        #self.log.debug('columnCount end')
        return len(self.keys)
    
    def data(self, index, role = None):
        ''' ''' 
        #self.log.debug('data start')
        if index.isValid():
            if index.row() >= 0 or index.row() < len(self.rows):
                if role == Qt.DisplayRole or role == Qt.ToolTipRole or role == Qt.EditRole:
                    return self.album.rows[index.row()][self.keys[index.column()]]
        #self.log.debug('data end')
        return QVariant()
    
    def setData(self, index, value, role):
        ''' ''' 
        #self.log.debug('setData start')
        if index.isValid() and role == Qt.EditRole:
            key = self.keys[index.column()]
            row = index.row()
            value = unicode(value.toString())
            self.album.rows[index.row()][key] = value
            self.emit(SIGNAL('dataChanged'), index, index)
        #self.log.debug('setData end')
        return True
    
    def headerData(self, section, orientation, role):
        ''' ''' 
        #self.log.debug('headerData start' + str(section))
        if section >= 0 and section < len(self.keys):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.keys[section]
        #self.log.debug('headerData end ')
        return QVariant()
    
    def flags(self, index):
        ''' ''' 
        #self.log.debug('flags start')
        if self.modelType == constants.ModelType.ModelTypeFinal:
            return super(QAbstractTableModel, self).flags(index) | Qt.ItemIsEditable
        #self.log.debug('flags end')
        return super(QAbstractTableModel, self).flags(index)
    
    def getModelType(self):
        ''' ''' 
        #self.log.debug('getModelType start')
        #self.log.debug('getModelType end')
        return self.modelType

    #def getState(self):
        #''' ''' 
        ##self.log.debug('getState start')
        ##self.log.debug('getState end')
        #return None
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    