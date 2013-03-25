from PyQt4 import QtGui
import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from jankflixmodules.cli.gui import JankflixForm
#change as necissary, and per your internet connection and caching status.
TIME_TO_WAIT = 200


class GuiTester(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.form = JankflixForm()
    def testFoo(self):
        self.failUnless(True)

    def testDisabledWatch(self):
        self.failIf(self.form.ui.myWatchPushButton.isEnabled(), "Watch is not disabled")

    def testDisabledSave(self):
        self.failIf(self.form.ui.mySavePushButton.isEnabled(), "Save is not disabled")

    def testDefaultLinkSite(self):
        self.failUnless(self.form.ui.my1ChannelRadioButton.isChecked(), "1channel is not the default link site")

    def testEnterText(self):
        query = "avatar"
        QTest.keyClicks(self.form.ui.mySearchLineEdit, query)
        self.assertEqual(self.form.ui.mySearchLineEdit.text(), query)

    # def testSearchForShow(self):
    #     query = "avatar"
    #     QTest.keyClicks(self.form.ui.mySearchLineEdit, query)
    #     self.assertEqual(self.form.ui.mySearchLineEdit.text(), query)
    #     self.setStatusBefore()
    #     QTest.keyClick(self.form.ui.mySearchLineEdit, Qt.Key_Return)
    #     self.assertStatusChanged()
    #     self.waitForListWidgetToChange(self.form.ui.myResultsListWidget)
    #     numResults = self.form.ui.myResultsListWidget.count()
    #     print numResults

    def setStatusBefore(self):
        self.statusBefore = self.form.ui.myStatusLabel.text()

    def assertStatusChanged(self):
        self.assert_(hasattr(self,"statusBefore"))
        self.failIfEqual(self.statusBefore, self.form.ui.myStatusLabel.text(), "Status did not change from: %s"
                                                                               %self.statusBefore)
        print "before %s after %s"%(self.statusBefore,self.form.ui.myStatusLabel.text())

    def waitForListWidgetToChange(self, listWidget):
        self.assertIsInstance(listWidget, QtGui.QListWidget)
        oldValues = map(lambda ind:listWidget.item(ind), range(listWidget.count()))
        for i in range(100):
            QTest.qSleep(TIME_TO_WAIT)
            newValues = map(lambda ind: listWidget.item(ind), range(listWidget.count()))
            print "old %s new %s"%(oldValues,newValues)
            if oldValues != newValues:
                return
        self.fail("Wait for list widget to change timed out")
