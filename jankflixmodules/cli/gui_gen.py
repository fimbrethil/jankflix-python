# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Fri Jan 25 11:19:18 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(705, 607)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 11, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 14, 0, 1, 2)
        self.myWatchPushButton = QtGui.QPushButton(Form)
        self.myWatchPushButton.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myWatchPushButton.sizePolicy().hasHeightForWidth())
        self.myWatchPushButton.setSizePolicy(sizePolicy)
        self.myWatchPushButton.setObjectName(_fromUtf8("myWatchPushButton"))
        self.gridLayout.addWidget(self.myWatchPushButton, 15, 0, 1, 1)
        self.myCancelPushButton = QtGui.QPushButton(Form)
        self.myCancelPushButton.setEnabled(False)
        self.myCancelPushButton.setObjectName(_fromUtf8("myCancelPushButton"))
        self.gridLayout.addWidget(self.myCancelPushButton, 16, 1, 1, 1)
        self.mySeasonListView = QtGui.QListView(Form)
        self.mySeasonListView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.mySeasonListView.setObjectName(_fromUtf8("mySeasonListView"))
        self.gridLayout.addWidget(self.mySeasonListView, 13, 0, 1, 1)
        self.myProgressBar = QtGui.QProgressBar(Form)
        self.myProgressBar.setEnabled(False)
        self.myProgressBar.setProperty("value", 0)
        self.myProgressBar.setTextVisible(True)
        self.myProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.myProgressBar.setObjectName(_fromUtf8("myProgressBar"))
        self.gridLayout.addWidget(self.myProgressBar, 16, 0, 1, 1)
        self.mySavePushButton = QtGui.QPushButton(Form)
        self.mySavePushButton.setEnabled(False)
        self.mySavePushButton.setObjectName(_fromUtf8("mySavePushButton"))
        self.gridLayout.addWidget(self.mySavePushButton, 15, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 12, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 12, 0, 1, 1)
        self.myEpisodeListView = QtGui.QListView(Form)
        self.myEpisodeListView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.myEpisodeListView.setObjectName(_fromUtf8("myEpisodeListView"))
        self.gridLayout.addWidget(self.myEpisodeListView, 13, 1, 1, 1)
        self.myResultsListView = QtGui.QListView(Form)
        self.myResultsListView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.myResultsListView.setObjectName(_fromUtf8("myResultsListView"))
        self.gridLayout.addWidget(self.myResultsListView, 3, 1, 6, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.mySearchLineEdit = QtGui.QLineEdit(Form)
        self.mySearchLineEdit.setObjectName(_fromUtf8("mySearchLineEdit"))
        self.gridLayout.addWidget(self.mySearchLineEdit, 3, 0, 1, 1)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.my1ChannelRadioButton = QtGui.QRadioButton(Form)
        self.my1ChannelRadioButton.setChecked(True)
        self.my1ChannelRadioButton.setObjectName(_fromUtf8("my1ChannelRadioButton"))
        self.horizontalLayout_3.addWidget(self.my1ChannelRadioButton)
        self.myTVLinksRadioButton = QtGui.QRadioButton(Form)
        self.myTVLinksRadioButton.setChecked(False)
        self.myTVLinksRadioButton.setObjectName(_fromUtf8("myTVLinksRadioButton"))
        self.horizontalLayout_3.addWidget(self.myTVLinksRadioButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 0, 1, 1)
        self.myStatusLabel = QtGui.QLabel(Form)
        self.myStatusLabel.setObjectName(_fromUtf8("myStatusLabel"))
        self.gridLayout.addWidget(self.myStatusLabel, 6, 0, 3, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Jankflix", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Search Results", None, QtGui.QApplication.UnicodeUTF8))
        self.myWatchPushButton.setText(QtGui.QApplication.translate("Form", "Watch", None, QtGui.QApplication.UnicodeUTF8))
        self.myCancelPushButton.setText(QtGui.QApplication.translate("Form", "Cancel Download", None, QtGui.QApplication.UnicodeUTF8))
        self.mySavePushButton.setText(QtGui.QApplication.translate("Form", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Episode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Season", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Search For TV Show", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Link site to search", None, QtGui.QApplication.UnicodeUTF8))
        self.my1ChannelRadioButton.setText(QtGui.QApplication.translate("Form", "1Channel", None, QtGui.QApplication.UnicodeUTF8))
        self.myTVLinksRadioButton.setText(QtGui.QApplication.translate("Form", "TVLinks", None, QtGui.QApplication.UnicodeUTF8))
        self.myStatusLabel.setText(QtGui.QApplication.translate("Form", "Status...", None, QtGui.QApplication.UnicodeUTF8))

