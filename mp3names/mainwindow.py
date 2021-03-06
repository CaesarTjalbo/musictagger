# -*- coding: utf-8 -*-
import sys
import os
import logging
import random

from functools import partial

import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import PyKDE4
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

import album_module
import config
import constants

#import mw_mainwindow
import ui_mainwindow
import dialog_module

import rulewidget

import tags
import utils_module
import model_classes
import rules_module


class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
    utils = utils_module.Utils()
    rules = rules_module.Rules()
    tags = tags.Tags()
    currentFileModel = None
    dialog = None
    rulesCheckState = None
    
    album = None
    currentSelectedDirectoryIndex = None
    
    def __init__(self, parent = None):
        ''' 
        ''' 
        self.log = logging.getLogger('MainWindow')
        #self.log.debug('__init__ start')
        super(MainWindow, self).__init__(parent)
        self.parent = parent
        
        #self.t = tcheckbox.TCheckBox(self)
        #self.t.setup()
        #styleSheet = self.styleSheet()
        #self.log.debug(styleSheet)
        #styleSheet = ''
        #self.log.debug('__init__ end')
        return None
    
    def setup(self):
        ''' 
        ''' 
        #self.log.debug('setup start')
        self.initFinalScreen = True # to prevent event from having effect
        self.storeSelfDefaultState() # remember the state of gui controls like checkBox and lineedits
        self._setup_dialogs()
        self._setup_actions()
        self._setup_buttons()
        self._setup_gui_elements()
        
        self.rules_list = self.rules.setup()
        self._setupRules(self.rules_list)
        #self.log.debug('setup end')
        return None
    
    def _setup_actions(self):
        ''' 
        ''' 
        #self.log.debug('_setup_actions start')
        #self.connect(self.actionChangeDirectory, SIGNAL("triggered()"), self._change_directory_action)
        self.connect(self.actionTreeViewDirectoryClicked, SIGNAL("triggered()"), self._treeViewDirectoryClicked)
        self.connect(self.actionTabChanged, SIGNAL("triggered()"), self._tabChanged)
        self.connect(self.actionTabDataChanged, SIGNAL("triggered()"), self._tabDataChanged)
        self.connect(self.actionSaveButtonClicked, SIGNAL("triggered()"), self._saveButtonClicked)
        self.connect(self.actionCheckBoxDataChanged, SIGNAL("triggered()"), self.resetAlbum)
        self.connect(self.actionLineEditChanged, SIGNAL("triggered()"), self._lineEditChanged)
        self.connect(self.actionFreeDataTextChanged, SIGNAL("triggered()"), self._freeDataTextChanged)
        self.connect(self.groupBox, SIGNAL("toggled(bool)"), self.toggleRules)
        #self.connect(self.pushButtonForceDeleteTags, SIGNAL("pressed()"), self.forceDeleteTags)
        self.connect(self.pushButtonArtistApplyRules, SIGNAL("pressed()"), self.applyRulesOnLineEdit)
        self.connect(self.pushButtonTitleApplyRules, SIGNAL("pressed()"), self.applyRulesOnLineEdit)
        self.connect(self.pushButtonDateApplyRules, SIGNAL("pressed()"), self.applyRulesOnLineEdit)
        self.connect(self.pushButtonCommentApplyRules, SIGNAL("pressed()"), self.applyRulesOnLineEdit)
        self.connect(self.comboBoxDisk, SIGNAL("currentIndexChanged(int)"), self.comboBoxDiskCurrentIndexChanged)
        
        #self.connect(self.checkBoxContinuousNumbering, SIGNAL("toggled(bool)"), self._checkBoxContinuousNumberingToggled)
        
        #self.log.debug('_setup_actions end')
        return None
    
    def _setup_buttons(self):
        ''' 
        ''' 
        #self.log.debug('_setup_buttons start')
        
        #self.log.debug('_setup_buttons end')
        return None
    
    def _setup_dialogs(self):
        ''' 
        ''' 
        #self.log.debug('_setup_dialogs start')
        self.dialog = dialog_module.SaveDialog(self.parent)
        self.dialog.setupUi(self.dialog)
        #self.log.debug(dir(self.dialog))
        #self.log.debug('_setup_dialogs end')
        return None
        
    def _setup_gui_elements(self):
        ''' 
        ''' 
        #self.log.debug('_setup_gui_elements start')
        
        # main window
        self.tabWidgetMainWindow.setCurrentIndex(0)
        #styleSheet = 'QTableView:enabled {color : red}'
        #self.setStyleSheet(styleSheet)
        
        # tab 0
        qfilesystemmodel = QFileSystemModel(self)
        basedir = QString(config.BASEDIRECTORY)
        qfilesystemmodel.setRootPath(basedir)
        self.treeViewDirectory.setModel(qfilesystemmodel)
        self.treeViewDirectory.setRootIndex(qfilesystemmodel.index(basedir))
        self.treeViewDirectory.setColumnWidth(0, 500)
        
        # tab 1 data
        self.tabWidgetData.setCurrentIndex(0)
        
        #self.lineEditDataArtist.setEnabled(True)
        #self.lineEditDataTitle.setEnabled(True)
        #self.lineEditDataDate.setEnabled(True)
        
        # readonly by default, only not when in 'free' mode
        #self.lineEditDataArtist.setReadOnly(True)
        #self.lineEditDataTitle.setReadOnly(True)
        #self.lineEditDataDate.setReadOnly(True)
        
        # tab 2 final
        #self.checkBoxArtist.setChecked(False)
        #self.checkBoxTitle.setChecked(False)
        #self.checkBoxDate.setChecked(False)
        #self.checkBoxComment.setChecked(False)
        #self.checkBoxVariousArtists.setChecked(False)
        self.groupBoxLayout = QVBoxLayout() # to hold the rules
        self.initFinalScreen = True
        #self.log.debug('_setup_gui_elements end')
        return None
        
    def _setupRules(self, rules_list):
        ''' fill the groupBox, groupBoxLayout with buttons and rules ''' 
        #self.log.debug('_setupRules start')
        resetButton = QPushButton(self.groupBox)
        resetButton.setText('Reset')
        resetButton.setToolTip('Reset the rules to their default state.')
        resetButton.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.connect(resetButton, SIGNAL("pressed()"), self.resetRules)
        self.groupBoxLayout.addWidget(resetButton)
        
        fixateButton = QPushButton(self.groupBox)
        fixateButton.setText('Fixate')
        fixateButton.setToolTip('Fixate current settings.\nReturn to a previous tab to undo.')
        fixateButton.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.connect(fixateButton, SIGNAL("pressed()"), self._fixateAlbum)
        self.groupBoxLayout.addWidget(fixateButton)
        
        self.minRuleNumber = self.groupBoxLayout.count()
        
        self.rulesCheckState = dict()
        for rule in rules_list:
            frame = QFrame(self.groupBox)
            frame.setObjectName('frame_' + rule.name)
            #frame.setFrameShape(QFrame.NoFrame)
            frame.setFrameShape(QFrame.Box)
            frame.setFrameShadow(QFrame.Plain)
            
            frame.setToolTip(rule.toolTip)
            frame.verticalLayout = QVBoxLayout(frame)
            frame.verticalLayout.setObjectName("verticalLayout")
            #frame.ruleWidget = QCheckBox(f)
            frame.ruleWidget = rulewidget.RuleWidget(frame)
            frame.ruleWidget.setObjectName("ruleWidget")
            frame.verticalLayout.addWidget(frame.ruleWidget)
            frame.rule = rule
            frame.ruleWidget.setText(rule.displayName)
            frame.ruleWidget.setChecked(rule.initially_checked)
            #self.connect(frame.ruleWidget, SIGNAL("toggled(bool)"), self._ruleToggled)
            self.connect(frame.ruleWidget, SIGNAL("toggled(bool)"), self.resetAlbum)
            self.connect(frame.ruleWidget, SIGNAL("moveUp()"), self.ruleMoveUp)
            self.connect(frame.ruleWidget, SIGNAL("moveDown()"), self.ruleMoveDown)
            
            if rule.needsInput:
                lineEdit = QLineEdit(frame)
                lineEdit.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
                frame.verticalLayout.addWidget(lineEdit)
                frame.rule.inputWidget = lineEdit
                self.connect(lineEdit, SIGNAL('editingFinished()'), self.resetAlbum)
                pass
            else:
                pass
            self.groupBoxLayout.addWidget(frame)
            
            self.rulesCheckState[frame.ruleWidget.objectName()] = frame.ruleWidget.isChecked()
        
        self.maxRuleNumber = self.groupBoxLayout.count()
        self.groupBoxLayout.addStretch(1)
        self.groupBox.setLayout(self.groupBoxLayout)
        #self.log.debug('_setupRules end')
        return None
    
    def getQDir(self, treeViewModel, treeViewIndex):
        ''' called from _treeViewDirectoryClicked & _saveButtonClicked''' 
        #self.log.debug('getQDir start')
        filters = QStringList()
        for extension in constants.EXTENSION_LIST:
            filters.append(QString('*.%s' % extension))
        
        qdir = QDir(treeViewModel.filePath(treeViewIndex))
        qdir.setNameFilters(filters)
        #self.log.debug('getQDir end')
        return qdir
    
    def loadAlbum(self, qdir):
        ''' called from _treeViewDirectoryClicked & _saveButtonClicked''' 
        #self.log.debug('loadAlbum start')
        album = album_module.Album(self)
        fileDataList = []
        if len(qdir.entryList()) < 1:
            #self.log.debug('NO ALBUM')
            return None
        else:
            for i, qs in enumerate(qdir.entryList()):
                #self.log.debug(qdir.filePath(qs))
                fileData = {'file' : qs
                            , 'path' : qdir.filePath(qs)
                            , 'directory' : qdir.dirName()
                            }
                fileDataList.append(fileData)
                
        album.directory = qdir.dirName()
        #self.log.debug(qdir.absolutePath())
        album.fullDirectory = qdir.absolutePath()
        album.setFileAndTagData(fileDataList)
        
        #self.log.debug('loadAlbum end')
        return album
    
    def _treeViewDirectoryClicked(self):
        ''' create an Album instance and fill data ''' 
        qdir = self.getQDir(self.treeViewDirectory.model(), self.treeViewDirectory.currentIndex())
        self.labelDirectory.setText(qdir.dirName())
        
        self.currentFileModel = QFileSystemModel()
        self.currentFileModel.setRootPath(qdir.absolutePath())
        
        self.album = self.loadAlbum(qdir)
        #self.log.debug('_treeViewDirectoryClicked end')
        return None

    def _tabChanged(self):
        ''' eventHandler for tabWidgetMainWindow
        ''' 
        log = logging.getLogger('%s._tabChanged' % self.log.name)
        #self.log.debug('tabChanged start')
        index = self.tabWidgetMainWindow.currentIndex()
        if index == 0: 
            # treeViewDirectory
            self.retrieveSelfDefaultState()
            
            # in case the 'free' mode was used, this seems an appropriate moment to clear the contents.
            self.textEditDataFree.setText('')
            
            self.tabFinal.setEnabled(False)
            if self.album:
                #if hasattr(self.album, 'model') and self.album.model:
                    
                    #self.album.model.album = None # remove circle reference
                    #self.album.model = None
                    
                model = self.album.getModelClass(constants.ModelType.ModelTypeNone)
                #self._setGuiAttributesOnAlbum()
                self.tableViewDataTags.setModel(model)
                self.tableViewFinal.setModel(model)
            else:
                #user should have selected an album here
                pass

        if index == 1:
            # data screen
            # reset screen
            self.retrieveSelfDefaultState()
            self.tableViewFinal.setModel(None)
            if self.album:
                self.tabFinal.setEnabled(True)
                self._tabDataChanged()
                #if hasattr(self.album, 'model'):
                    #if self.album.model:
                        #if self.album.modelType != constants.ModelType.ModelTypeNone:
                            ## fill screen
                            ##log.debug('data tab modelType: %s' % constants.ModelType.getNameFromType(self.album.modelType))
                            #pass
                        #else:
                            ##log.debug('tab 1 ModelType == ModelTypeNone')
                            #pass
                    #else:
                        ##log.debug('tab 1, model is None')
                        #pass
                    #pass
                #else:
                    ##log.debug('tab 1, no model')
                    #pass
            else:
                #log.debug('tab 1, no album')
                # empty screen, empty final screen
                self.tableViewDataTags.setModel(None)
                self.tabFinal.setEnabled(False)
                #pass
        if index == 2: # final
            #self.log.debug('================== final tab ========================')
            #clear the screens
            self.retrieveSelfDefaultState()
            
            if self.album:
                if hasattr(self.album, 'model'):
                    if self.album.model:
                        #log.debug('final tab modelType: %s' % constants.ModelType.getNameFromType(self.album.modelType))
                        if self.album.modelType != constants.ModelType.ModelTypeNone:
                            dataindex = self.tabWidgetData.currentIndex()
                            if dataindex == 0: 
                                # from file and from tags, see _tabDataChanged
                                pass
                            if dataindex == 1: # from free
                                if self.album.model:
                                    #self.log.debug('free')
                                    ''' reading all the data from the screen, trying to make sense of it, filling final screen with what we find '''
                                    #self.logAlbum('1')
                                    #log.debug(self.lineEditDataArtist.text())
                                    #log.debug(self.lineEditDataTitle.text())
                                    #log.debug(self.lineEditDataDate.text())
                                    
                                    self.album.albumArtist = self.lineEditDataArtist.text()
                                    self.album.albumTitle = self.lineEditDataTitle.text()
                                    self.album.albumDate = self.lineEditDataDate.text()
                                    self.album.albumComment = self.lineEditFinalComment.text()
                                    #self.logAlbum('2')
                                    
                                    # force the event in case the user re-visits the tab without changing text
                                    self._freeDataTextChanged()
                            
                            if self.album:
                                #self.log.debug('has model')
                                #self.log.debug(self.initFinalScreen)
                                model = self.album.getModelClass(constants.ModelType.ModelTypeFinal)
                                #self._setGuiAttributesOnAlbum()
                                #self.album.modelType = constants.ModelType.ModelTypeFinal
                                #self.logAlbum(37)
                                self.initFinalScreen = True # used to prevent events having effect when controls are filled
                                #self._ruleToggled()
                                self.lineEditFinalArtist.setText(self.album.albumArtist)
                                self.lineEditFinalTitle.setText(self.album.albumTitle)
                                self.lineEditFinalDate.setText(self.album.albumDate)
                                self.lineEditFinalComment.setText(self.album.albumComment)
                                self.initFinalScreen = False
                                self.resetAlbum()
                                #self.logAlbum(39)
                            
                                #self.tableViewFinal.setModel(model)
                                #self.tableViewFinal.resizeColumnsToContents()
                        else:
                            #self.log.debug('_tabChanged, modelType = ModelType.ModelTypeNone')
                            pass
                    else:
                        #self.log.debug('_tabChanged, model = None')
                        # eh
                        pass
                else:
                    #self.log.debug('_tabChanged, no model')
                    #something must have gone wrong in the second tab
                    pass
            else:
                #self.log.debug('_tabChanged, no album')
                #something must have gone wrong in the first tab
                pass
        #self.log.debug('tabChanged end')
        return None
    
    def _tabDataChanged(self):
        ''' eventHandler for tabWidgetData
        handle the screen where the user selects between data from tags, files or free input
        called by method _tabChanged and on event when a tab changes ''' 
        log = logging.getLogger('%s._tabDataChanged' % self.log.name)
        #log.debug('_tabDataChanged start')
        if self.album:
            #self.log.debug('here')
            dataindex = self.tabWidgetData.currentIndex()
            #model = None
            if dataindex == 0:
                self.lineEditDataArtist.setReadOnly(True)
                self.lineEditDataTitle.setReadOnly(True)
                self.lineEditDataDate.setReadOnly(True)
                model = None
                if self.radioButtonFiles.isChecked():
                    #self.log.debug('files')
                    model = self.album.getModelClass(constants.ModelType.ModelTypeFiles)
                    
                if self.radioButtonTags.isChecked():
                    #self.log.debug('tags')
                    model = self.album.getModelClass(constants.ModelType.ModelTypeTags)
                if not model:
                    self.log.error('wtf, radioButton error')
                #self._setGuiAttributesOnAlbum()
                self.tableViewDataTags.setModel(model)
                self.tableViewDataTags.resizeColumnsToContents()
                    
            if dataindex == 1:
                if self.album:
                    self.lineEditDataArtist.setReadOnly(False)
                    self.lineEditDataTitle.setReadOnly(False)
                    self.lineEditDataDate.setReadOnly(False)
                    model = self.album.getModelClass(constants.ModelType.ModelTypeFree)
                    #self._setGuiAttributesOnAlbum()
                    self.labelNumberOfTracks.setText('%03d' % len(self.album.rows))
                    self._freeDataTextChanged()
                else:
                    self.log.debug('dataindex == 1, ever reached?')
            
            self.lineEditDataArtist.setText(self.album.albumArtist)
            self.lineEditDataTitle.setText(self.album.albumTitle)
            self.lineEditDataDate.setText(self.album.albumDate)
        else:
            # no album selected
            pass
        
        #try:
            #log.debug('data tab modelType: %s' % constants.ModelType.getNameFromType(self.album.modelType))
        #except Exception:
            #log.debug('blub')
            #pass
        #self.log.debug('_tabDataChanged end')
        return None
    
    
    def _saveButtonClicked(self):
        ''' eventHandler for the save button
        ''' 
        #self.log.debug('_saveButtonClicked start')
        
        albumArtist = self.lineEditFinalArtist.text()
        albumTitle = self.lineEditFinalTitle.text()
        albumDate = self.lineEditFinalDate.text()
        albumComment = self.lineEditFinalComment.text()
        various_artists = self.checkBoxVariousArtists.isChecked()
        continous_numbering = self.checkBoxContinuousNumbering.isChecked()
        volumeString = self.comboBoxDisk.currentText()
        self.log.debug('albumArtist: "%s"' % albumArtist)
        self.log.debug('albumTitle: "%s"' % albumTitle)
        self.log.debug('albumDate: "%s"' % albumDate)
        self.log.debug('albumComment: "%s"' % albumComment)
        self.log.debug('various_artists: "%s"' % various_artists)
        self.log.debug('continous_numbering: "%s"' % continous_numbering)
        self.log.debug('volumeString: "%s"' % volumeString)
        
        
        result, newDirectoryName = self.album.save()
        if result:
            self.log.debug('Save succeeded')
            
            #------------
            fileSystemModel = self.treeViewDirectory.model()
            index = fileSystemModel.setRootPath(QString(newDirectoryName))
            fileSystemModel.reset()
            self.treeViewDirectory.setRootIndex(fileSystemModel.index(QString(config.BASEDIRECTORY)))
            self.treeViewDirectory.setCurrentIndex(index)
            qdir = self.getQDir(fileSystemModel, index)
            #------------
            
            self.album = self.loadAlbum(qdir)
            self.album.getModelClass(constants.ModelType.ModelTypeTags)
            model = self.album.getModelClass(constants.ModelType.ModelTypeFinal)
            
            #self.log.debug(self.album.rows)
        
        #self.log.debug('_saveButtonClicked end')
        return None
        
    def _lineEditChanged(self):
        ''' eventHandler for the lineedits in final screen ''' 
        #self.log.debug('_lineEditChanged start')
        if self.initFinalScreen:
            #self.log.debug('_lineEditChanged ignored')
            pass
        else:
            if self.album:# and self.album.model:
                #self.log.debug('_lineEditChanged busy')
                self.album.albumArtist = self.lineEditFinalArtist.text()
                self.album.albumTitle = self.lineEditFinalTitle.text()
                self.album.albumDate = self.lineEditFinalDate.text()
                self.album.albumComment = self.lineEditFinalComment.text()
                self.logAlbum('_lineEditChanged ')
                #self.updateFinalScreen()
                self.resetAlbum()
        #self.log.debug('_lineEditChanged end')
        return None
    
    def comboBoxDiskCurrentIndexChanged(self):
        ''' ''' 
        #log = logging.getLogger('%s.comboBoxDiskCurrentIndexChanged' % self.log.name)
        self.log.debug('comboBoxDiskCurrentIndexChanged start')
        if self.album:
            self.album.volumeString = unicode(self.comboBoxDisk.currentText())
        #self.log.debug('comboBoxDiskCurrentIndexChanged end')
        return None
    
    def logAlbum(self, param = ''):
        ''' 
        ''' 
        #self.log.debug('logAlbum start')
        self.log.debug(str(param) + self.album.albumArtist)
        self.log.debug(str(param) + self.album.albumTitle)
        self.log.debug(str(param) + self.album.albumDate)
        self.log.debug(str(param) + self.album.albumComment)
        
        #self.log.debug('logAlbum end')
        return None
        
    def resetAlbum(self, execute = True):
        ''' resets data in album to previous stored data
        used to roll back effects from edits and rules
        should only be called from the final tab ''' 
        #self.log.debug('resetAlbum start')
        #self.logAlbum()
        if self.album:
            self.album.reset()
        #self.log.debug('resetAlbum')
        self.setGuiAttributesOnAlbum()
        self.executeRules()
        self.updateFinalScreen()
        #self.logAlbum()
        #self.log.debug('resetAlbum end')
        return None
    
    def setGuiAttributesOnAlbum(self):
        ''' central methode to force song attributes to use the text from the lineedits ''' 
        #self.log.debug('setGuiAttributesOnAlbum start')
        self.album.useAlbumArtist = self.checkBoxArtist.isChecked()
        self.album.useAlbumTitle = self.checkBoxTitle.isChecked()
        self.album.useAlbumDate = self.checkBoxDate.isChecked()
        self.album.useAlbumComment = self.checkBoxComment.isChecked()
        self.album.useAlbumVariousArtists = self.checkBoxVariousArtists.isChecked()
        self.album.useAlbumContinuousNumbering = self.checkBoxContinuousNumbering.isChecked()
        #self.album.useAlbumTotalTracks = self.checkBoxTotalTracks.isChecked()
        
        #self.log.debug('setGuiAttributesOnAlbum end')
        return None
    
    def executeRules(self):
        ''' 
        ''' 
        #self.log.debug('executeRules start')
        l = self.groupBox.children()
        #self.log.debug(len(l))
        
        # loop through gui elements to retrieve properties
        for frame in l:
            #self.log.debug('** ' + str(type(frame)))
            #if hasattr(frame, 'rule'):
            if type(frame) == QFrame:
                #self.log.debug(frame.rule.displayName)
                #if frame.objectName() == 'frame_Rule_SwapArtistTitle':
                    #s = '%s isChecked(%s)'
                    #self.log.debug(s % (frame.objectName(), frame.ruleWidget.isChecked()))
                frame.rule.checked = frame.ruleWidget.isChecked()
                #if frame.rule.name == 'Rule_SwapArtistTitle':
                    #s = '%s isChecked(%s)'
                    #self.log.debug(s % (frame.rule.name, frame.rule.checked))
                if frame.rule.needsInput and not frame.ruleWidget.isChecked():
                    frame.rule.inputWidget.setText('')
                if frame.rule.allRows:
                    frame.rule.setRows(self.album.rows)
        
        # loop through rules and execute each
        for rule in self.rules_list:
            #if rule.name == 'Rule_SwapArtistTitle':
                #s = '%s isChecked(%s)'
                #self.log.debug(s % (rule.name, rule.checked))
            
            if rule.checked:
                #if rule.name == 'Rule_SwapArtistTitle':
                    #self.log.debug('here')
                for row in self.album.rows:
                    rule.execute(row)
                    
        #for frame in l:
            #if type(frame) == QFrame:
                #if frame.rule.executeOnce:
                    #frame.rule.checked = False
                    #frame.ruleWidget.setChecked(False)
       
        #self.log.debug('executeRules end')
        return None
    
    def updateFinalScreen(self):
        ''' refreshes the data on final screen ''' 
        #self.log.debug('updateFinalScreen start')
        self.lineEditFinalArtist.setText(self.album.albumArtist)
        self.lineEditFinalTitle.setText(self.album.albumTitle)
        self.lineEditFinalDate.setText(self.album.albumDate)
        self.lineEditFinalComment.setText(self.album.albumComment)
        self.tableViewFinal.setModel(self.album.model)
        if self.album.model:
            self.album.model.reset()
        self.tableViewFinal.resizeColumnsToContents()
        
        #self.log.debug('updateFinalScreen end')
        return None
    
    def _fixateAlbum(self):
        ''' stores the data as is set, provides a roll abck point for reset
        ''' 
        #self.log.debug('_fixateAlbum start')
        if self.album:
            self.album.fixate()
        #self.log.debug('_fixateAlbum end')
        return None
    
    def resetRules(self):
        ''' eventHandler for the reset rules button ''' 
        #self.log.debug('resetRules start')
        l = self.groupBox.children()
        for frame in l:
            if type(frame) == QFrame:
                frame.rule.checked = frame.rule.initially_checked
                frame.ruleWidget.setChecked(frame.rule.checked)
                if frame.rule.needsInput and not frame.ruleWidget.isChecked():
                    frame.rule.inputWidget.setText('')
        
        self.resetAlbum()
        #self.log.debug('resetRules end')
        return None
    
    #def _checkBoxVariousArtistsToggled(self):
        #''' 
        #''' 
        ##self.log.debug('_checkBoxVariousArtistsToggled start')
        ##self.album.useAlbumVariousArtists
        #self.album.useAlbumVariousArtists = self.checkBoxVariousArtists.isChecked()
        ##self.lineEditDataArtist.setEnabled(False)
        ##self.log.debug('_checkBoxVariousArtistsToggled end')
        #return None
    
    def storeSelfDefaultState(self):
        ''' 
        ''' 
        #self.log.debug('storeSelfDefaultState start')
        self.attributes = dict()
        for a in self.__dict__.keys():
            if type(self.__dict__[a]) is QLineEdit:
                # we don't want the lineedits in the Data screen
                if a.find('Data')  == -1:
                    #self.log.debug(unicode(a))
                    o = self.__dict__[a]
                    d = dict()
                    d['isEnabled'] = o.isEnabled()
                    d['isReadOnly'] = o.isReadOnly()
                    d['text'] = o.text()
                    self.attributes[a] = d
        for a in self.__dict__.keys():
            if type(self.__dict__[a]) is QCheckBox:
                #self.log.debug(unicode(a))
                o = self.__dict__[a]
                d = dict()
                d['isEnabled'] = o.isEnabled()
                d['isChecked'] = o.isChecked()
                self.attributes[a] = d
        #self.log.debug('storeSelfDefaultState end')
        return None
    
    def retrieveSelfDefaultState(self):
        ''' 
        ''' 
        #self.log.debug('getSelfDefaultState start')
        for o in self.attributes.keys():
            #self.log.debug('%s' % o)
            
            for a in self.attributes[o].keys():
                if a == 'isEnabled':
                    self.__dict__[o].setEnabled(self.attributes[o][a])
                if a == 'isReadOnly':
                    self.__dict__[o].setReadOnly(self.attributes[o][a])
                if a == 'isChecked':
                    self.__dict__[o].setChecked(self.attributes[o][a])
                if a == 'text':
                    self.__dict__[o].setText(self.attributes[o][a])
                    
                #self.log.debug('%s %s' % (o, a))
                #self.__dict__[o][a] = o[a]
        #self.log.debug('getSelfDefaultState end')
        return None
    
    def _freeDataTextChanged(self):
        ''' ''' 
        log = logging.getLogger('%s._freeDataTextChanged' % self.log.name)
        #self.log.debug('_freeDataTextChanged start')
        if self.album:
            #for row in self.album.rows:
                #log.debug(row)
                
            songs = list()
            t = unicode(self.textEditDataFree.toPlainText()).strip()
            t_list = t.split('\n')
            for t in t_list:
                result = self.utils.getSongDataFromFileName(t)
                result['comment'] = ''
                result['album'] = ''
                result['date'] = ''
                #result['album'] = self.lineEditDataTitle.text()
                #result['date'] = self.lineEditDataDate.text()
                #self.log.debug(self.album.model.keys)
                songs.append(result)
                #log.debug(result)
            #self.album.rows = self.utils.changeDictsToLists(songs, constants.TABLE_KEYS)
            if len(songs) >= len(self.album.rows):
                rowCount = len(self.album.rows)
            else:
                rowCount = len(songs)
            for i in range(rowCount):
                for key in songs[i].keys():
                    if key in ['extension', 'filename', 'path']:
                        pass
                    else:
                        self.album.rows[i][key] = songs[i][key]
            #else:   
                #self.album.rows = songs
            #for row in self.album.rows:
                #log.debug(row)
                
            if len(t_list) == len(self.album.rows):
                self.kledNumberOfTracks.setColor(Qt.green)
            else:
                self.kledNumberOfTracks.setColor(Qt.red)

        else:
            #log.debug('no album')
            pass
            
        #self.log.debug('_freeDataTextChanged end')
        return None
    
    def blah(self, message):
        ''' ''' 
        log = logging.getLogger('%s.blah' % self.log.name)
        #self.log.debug('blah start')
        red = '<font color="Red">'
        green = '<font color="Green">'
        blue = '<font color="Blue">'
        end = '</font>'
        succeeded = '%s%s%s' % (green, 'Success', end)
        failed = '%s%s%s' % (red, 'Failed', end)
        #title = '%s%s%s' % (blue, 'Success', end)
        if type(message) is tuple:
            if message[1] == None:
                message = '%s%s%s' % (blue, message[0], end)
            else:
                if message[1]:
                    message = '%s: %s' % (message[0], succeeded)
                else:
                    message = '%s: %s' % (message[0], failed)
        
        t = self.dialog.textEditResults.toHtml()
        self.dialog.textEditResults.setText(t.append(message))
        #log.debug(message)
        #self.log.debug('blah end')
        return None
    
    def showSaveDialog(self):
        ''' ''' 
        log = logging.getLogger('%s.showSaveDialog' % self.log.name)
        #log.debug('showSaveDialog start')
        self.dialog.textEditResults.setText('')
        self.dialog.show()
        
        #self.log.debug('blup end')
        return None
    
    def forceDeleteTags(self):
        ''' obsolete''' 
        #log = logging.getLogger('%s.forceDeleteTags' % self.log.name)
        #self.log.debug('forceDeleteTags start')
        if self.album:
            self.album.forceDeleteTags()
        #self.log.debug('forceDeleteTags end')
        return None
    
    def ruleMoveUp(self):
        ''' ''' 
        #log = logging.getLogger('%s.ruleMoveUp' % self.log.name)
        #self.log.debug('ruleMoveUp start')
        i = self.groupBoxLayout.indexOf(self.sender().parent)
        if i > self.minRuleNumber:
            self.groupBoxLayout.removeWidget(self.sender().parent)
            self.groupBoxLayout.insertWidget( i - 1, self.sender().parent)
        
        
        self.resetAlbum()
        #self.log.debug('ruleMoveUp end')
        return None
    
    def ruleMoveDown(self):
        ''' ''' 
        log = logging.getLogger('%s.ruleMoveDown' % self.log.name)
        #self.log.debug('ruleMoveDown start')
        #self.log.debug(self.sender().objectName())
        i = self.groupBoxLayout.indexOf(self.sender().parent)
        #log.debug(i)
        if i < self.maxRuleNumber - 1:
            self.groupBoxLayout.removeWidget(self.sender().parent)
            self.groupBoxLayout.insertWidget( i + 1, self.sender().parent)
        
        self.resetAlbum()
        #self.log.debug('ruleMoveDown end')
        return None
    
    def applyRulesOnLineEdit(self):
        ''' ''' 
        #log = logging.getLogger('%s.applyRulesOnLineEdit' % self.log.name)
        #self.log.debug('applyRulesOnLineEdit start')
        d = dict()
        if self.sender().objectName() == 'pushButtonArtistApplyRules':
            d['artist'] = unicode(self.lineEditFinalArtist.text())
            
        if self.sender().objectName() == 'pushButtonTitleApplyRules':
            d['album'] = unicode(self.lineEditFinalTitle.text())
            
        if self.sender().objectName() == 'pushButtonDateApplyRules':
            d['date'] = unicode(self.lineEditFinalDate.text())
            
        if self.sender().objectName() == 'pushButtonCommentApplyRules':
            d['comment'] = unicode(self.lineEditFinalComment.text())
        
        if len(d) == 1:
            key = d.keys()[0]
            for frame in self.groupBox.children():
                if type(frame) == QFrame:
                    if frame.rule.checked:
                        if frame.rule.allRows:
                            frame.rule.setRows(self.album.rows)
                        #self.log.debug(d)
                        d = frame.rule.execute(d)
                        #self.log.debug(d)
            
            if key == 'artist':
                self.lineEditFinalArtist.setText(d[key])
            if key == 'album':
                self.lineEditFinalTitle.setText(d[key])
            if key == 'date':
                self.lineEditFinalDate.setText(d[key])
            if key == 'comment':
                self.lineEditFinalComment.setText(d[key])
        else:
            self.log.debug('applyRulesOnLineEdit: # of keys: %d' % len(d))
        #self.log.debug('applyRulesOnLineEdit end')
        return None
    
    def toggleRules(self):
        ''' ''' 
        #log = logging.getLogger('%s.toggleRules' % self.log.name)
        #self.log.debug('toggleRules start')
        if self.groupBox.isChecked():
            for frame in self.groupBox.children():
                if type(frame) == QFrame:
                    frame.rule.checked = self.rulesCheckState[frame.objectName()] 
                    frame.ruleWidget.setChecked(self.rulesCheckState[frame.objectName()])
        else:
            for frame in self.groupBox.children():
                if type(frame) == QFrame:
                    self.rulesCheckState[frame.objectName()] = frame.ruleWidget.isChecked()
                    frame.rule.checked = False 
                    frame.ruleWidget.setChecked(False)
            
            
        self.resetAlbum()
        
        #self.log.debug('toggleRules end')
        return None
    
    
    
'''
app starts, we hebben nog niks.
_treeViewDirectoryClicked
we hebben mogelijk een album


_tabChanged:
geen album: scherm leeg, final scherm leeg

_tabChanged tab = 0
we zijn (terug) op het directory scherm

_tabChanged tab = 1
we hebben geen album:
scherm leeg, final scherm leeg

we hebben een album:
vul scherm met data via het model







'''
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
     
    
     
    
     
    
     
    
     
    
     
    
     
    
     
    
     
    
     
    
     
    
    
   
   
   
   
   
   
   
   
   
   
   
   
    
    
    
    
    
    
        