# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Mon Mar 18 23:51:09 2013
#      by: PyQt4 UI code generator 4.9.3
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
        Form.resize(646, 604)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.myWatchPushButton = QtGui.QPushButton(Form)
        self.myWatchPushButton.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myWatchPushButton.sizePolicy().hasHeightForWidth())
        self.myWatchPushButton.setSizePolicy(sizePolicy)
        self.myWatchPushButton.setObjectName(_fromUtf8("myWatchPushButton"))
        self.gridLayout.addWidget(self.myWatchPushButton, 16, 0, 1, 1)
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
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 12, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 12, 0, 1, 1)
        self.myDownloadGridLayout = QtGui.QGridLayout()
        self.myDownloadGridLayout.setObjectName(_fromUtf8("myDownloadGridLayout"))
        self.gridLayout.addLayout(self.myDownloadGridLayout, 19, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 15, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 11, 0, 1, 2)
        self.mySavePushButton = QtGui.QPushButton(Form)
        self.mySavePushButton.setEnabled(False)
        self.mySavePushButton.setObjectName(_fromUtf8("mySavePushButton"))
        self.gridLayout.addWidget(self.mySavePushButton, 16, 1, 1, 1)
        self.textBrowser = QtGui.QTextBrowser(Form)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 14, 0, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 17, 0, 1, 2)
        self.myResultsListWidget = QtGui.QListWidget(Form)
        self.myResultsListWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.myResultsListWidget.setObjectName(_fromUtf8("myResultsListWidget"))
        self.gridLayout.addWidget(self.myResultsListWidget, 3, 1, 6, 1)
        self.myEpisodeListWidget = QtGui.QListWidget(Form)
        self.myEpisodeListWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.myEpisodeListWidget.setObjectName(_fromUtf8("myEpisodeListWidget"))
        self.gridLayout.addWidget(self.myEpisodeListWidget, 13, 1, 1, 1)
        self.mySeasonListWidget = QtGui.QListWidget(Form)
        self.mySeasonListWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.mySeasonListWidget.setObjectName(_fromUtf8("mySeasonListWidget"))
        self.gridLayout.addWidget(self.mySeasonListWidget, 13, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Jankflix", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Search For TV Show", None, QtGui.QApplication.UnicodeUTF8))
        self.myWatchPushButton.setText(QtGui.QApplication.translate("Form", "Watch", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Link site to search", None, QtGui.QApplication.UnicodeUTF8))
        self.my1ChannelRadioButton.setText(QtGui.QApplication.translate("Form", "1Channel", None, QtGui.QApplication.UnicodeUTF8))
        self.myTVLinksRadioButton.setText(QtGui.QApplication.translate("Form", "TVLinks", None, QtGui.QApplication.UnicodeUTF8))
        self.myStatusLabel.setText(QtGui.QApplication.translate("Form", "Status...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Search Results", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Episode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Season", None, QtGui.QApplication.UnicodeUTF8))
        self.mySavePushButton.setText(QtGui.QApplication.translate("Form", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

