# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_saved.ui'
#
# Created: Sun Jun  2 15:18:14 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialogSaved(object):
    def setupUi(self, DialogSaved):
        DialogSaved.setObjectName(_fromUtf8("DialogSaved"))
        DialogSaved.setWindowModality(QtCore.Qt.WindowModal)
        DialogSaved.resize(966, 647)
        DialogSaved.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(DialogSaved)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEditResults = QtGui.QTextEdit(DialogSaved)
        self.textEditResults.setFrameShape(QtGui.QFrame.Box)
        self.textEditResults.setFrameShadow(QtGui.QFrame.Plain)
        self.textEditResults.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textEditResults.setReadOnly(True)
        self.textEditResults.setObjectName(_fromUtf8("textEditResults"))
        self.gridLayout.addWidget(self.textEditResults, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(493, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonClose = QtGui.QPushButton(DialogSaved)
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))
        self.horizontalLayout.addWidget(self.pushButtonClose)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(DialogSaved)
        QtCore.QObject.connect(self.pushButtonClose, QtCore.SIGNAL(_fromUtf8("clicked()")), DialogSaved.close)
        QtCore.QMetaObject.connectSlotsByName(DialogSaved)

    def retranslateUi(self, DialogSaved):
        DialogSaved.setWindowTitle(QtGui.QApplication.translate("DialogSaved", "Saving", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonClose.setText(QtGui.QApplication.translate("DialogSaved", "Close", None, QtGui.QApplication.UnicodeUTF8))

