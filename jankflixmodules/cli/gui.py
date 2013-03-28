from PyQt4 import QtCore, QtGui
import functools
from gui_gen import Ui_Form
from jankflixmodules.cli.downloader import ProgressCancel
from jankflixmodules.site import hostsitepicker
from jankflixmodules.site.linksite.onechannel import OneChannel
from jankflixmodules.site.linksite.tvlinks import TVLinks
import os
import subprocess
import sys
import time
import types


'''
Prefetch search key for link site(s), also serves as warmup request.
Do ALL web requests and logic in general in a separate thread. This includes running initial search, finding a good host site, etc.
Have a configuration file for common stuff (where to save to, file name pattern)
Remember/cache on disk last search and results (aka if I just watched season 2 episode 6 of Game of Thrones, when I open it back up, have the linksite search results open with the correct one selected, the correct season selected, and the correct, or next, episode selected, all without any web queries)
ability to download multiple at once/get a season
Playlists or continuous play
When naming, use proper show name as given by linksite (capitalized and all)
Give priority to certain sites/faster downloads. Possibly start the download on a few sites and only use the one that's going the fastest
Ability to show/submit captcha's and/or support vidxden
'''

class JankflixForm(QtGui.QWidget):
    def __init__(self, parent=None):
        super(JankflixForm, self).__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.mySearchLineEdit.returnPressed.connect(self.handleRunQuery)
        self.ui.my1ChannelRadioButton.clicked.connect(lambda: self.handleRadioButton("1channel"))
        self.ui.myTVLinksRadioButton.clicked.connect(lambda: self.handleRadioButton("tvlinks"))
        self.ui.myResultsListWidget.clicked.connect(self.handleChoseResult)
        self.ui.mySeasonListWidget.clicked.connect(self.handleChoseSeason)
        self.ui.myEpisodeListWidget.clicked.connect(self.handleChoseEpisode)
        self.ui.mySavePushButton.clicked.connect(self.handleSave)
        self.ui.myWatchPushButton.clicked.connect(self.handleOpen)
        self.ui.mySearchLineEdit.setFocus()

        self.myDownloadThread = None
        self.myWebRequestThread = None
        self.myFilename = None

        if self.ui.myTVLinksRadioButton.isChecked():
            self.myAreResultsTvLinks = True
        else:
            self.myAreResultsTvLinks = False
        # if not hasattr(self, "prefetchedKey") or self.prefetchedKey is not None:
        #     self.createWebRequestThread(self.setPrefetchedKey, OneChannel.prefetchSearchKey)
        self.setPrefetchedKey(None)
        self.pc = ProgressCancel(self, self.ui.myProgressCancelVerticalLayout)

    def setPrefetchedKey(self, key):
        self.prefetchedKey = key

    def createWebRequestThread(self, updateMethod, httpMethod, *args, **kwargs):
        """
        A way to make web calls without blocking the gui thread.
        @param updateMethod: Method to be called when the result is available. Will be called with the result as an arg.
        @param httpMethod: Method to be called asynchronously. After this is done, updateMethod is called.
        @param args: Args to be fed into httpMethod
        @param kwargs: optional listWidget or textBrowser to insert elipses into to indicate loading
        """
        #the or is because both updateMethod and httpMethod can be either methods specified in the class
        #or lambdas specified in the calling method
        assert isinstance(updateMethod, types.FunctionType) or isinstance(updateMethod, types.MethodType), \
            ("type is actually %s", type(updateMethod))
        assert isinstance(httpMethod, types.FunctionType) or isinstance(httpMethod, types.MethodType) \
            or isinstance(httpMethod, functools.partial), ("type is actually %s", type(httpMethod))
        assert isinstance(args, tuple)
        #if any webrequest is running, terminate it and start this one instead
        lvwidg = "listWidget"
        tb = "textBrowser"
        if lvwidg in kwargs:
            listWidget = kwargs[lvwidg]
            assert isinstance(listWidget, QtGui.QListWidget)
            self.updateListWidget(["..."], listWidget)
        elif tb in kwargs:
            textBrowser = kwargs[tb]
            assert isinstance(textBrowser, QtGui.QTextBrowser)
            textBrowser.setText("...")

        if self.myWebRequestThread is not None:
            self.myWebRequestThread.terminate()
        wrThread = WebRequestThread(self, httpMethod, *args)
        self.connect(wrThread, wrThread.updateListSignal, updateMethod)
        self.myWebRequestThread = wrThread
        wrThread.start()

    def updateSearchResults(self, runQueryResult):
        assert isinstance(runQueryResult, list)
        assert len(runQueryResult) > 0
        for result in runQueryResult:
            assert isinstance(result, tuple)
            assert len(result) == 2
            assert isinstance(result[0], str)
            assert isinstance(result[1], str)

        data = [name_url[0] for name_url in runQueryResult]
        self.updateListWidget(data, self.ui.myResultsListWidget)
        self.myQueryResult = runQueryResult
        #automatically select first result regardless of the number of search results
        item = self.ui.myResultsListWidget.item(0)
        self.ui.myResultsListWidget.setItemSelected(item, True)
        self.handleChoseResult()

    def updateListWidget(self, data, listWidget):
        assert isinstance(listWidget, QtGui.QListWidget)
        assert isinstance(data, list)
        assert len(data) > 0

        listWidget.clear()
        for element in data:
            listWidget.addItem(str(element))

    def updateStatus(self, status):
        assert isinstance(status, str)

        self.ui.myStatusLabel.setText(status)

    def getFirstSelectedIndex(self, ListWidget):
        assert isinstance(ListWidget, QtGui.QListWidget)

        indecies = ListWidget.selectedIndexes()
        if len(indecies) > 0:
            #gets the row of the selected value
            resultIndex = indecies[0].row()
            return resultIndex

    def getFirstSelectedItem(self, listWidget):
        assert isinstance(listWidget, QtGui.QListWidget)

        index = self.getFirstSelectedIndex(listWidget)
        print "first selected index returns %d" % (index)
        if index is not None:
            return listWidget.item(index)

    def handleRadioButton(self, whichButton):
        assert isinstance(whichButton, str)

        self.ui.mySavePushButton.setEnabled(False)
        self.ui.myWatchPushButton.setEnabled(False)
        if whichButton == "tvlinks":
            self.myAreResultsTvLinks = True
        else:
            self.myAreResultsTvLinks = False
        self.handleRunQuery()

    def handleRunQuery(self):
        self.myQuery = str(self.ui.mySearchLineEdit.text())
        if len(self.myQuery) > 0:
            self.ui.mySavePushButton.setEnabled(False)
            self.ui.myWatchPushButton.setEnabled(False)
            #create result depending on which linksite was checked
            if self.myAreResultsTvLinks:
                self.updateStatus("Searching TVLinks for %s" % (self.myQuery))
                self.createWebRequestThread(self.updateSearchResults, TVLinks.searchSite, self.myQuery, listWidget=self.ui.myResultsListWidget)
            else:
                self.updateStatus("Searching OneChannel for %s" % (self.myQuery))
                if self.prefetchedKey is None:
                    print "not prefetched key"
                    searchMethod = OneChannel.searchSite
                else:
                    print "using prefetched key"
                    searchMethod = lambda query: OneChannel.searchSite(query, self.prefetchedKey)
                self.createWebRequestThread(self.updateSearchResults, searchMethod, self.myQuery, listWidget=self.ui.myResultsListWidget)

    def handleChoseResult(self):
        index = self.getFirstSelectedIndex(self.ui.myResultsListWidget)
        if index is None:
            return
        self.ui.mySavePushButton.setEnabled(False)
        self.ui.myWatchPushButton.setEnabled(False)
        url = self.myQueryResult[index][1]
        #            instansiate myLinkSite with correct
        #            this avoids the condition where the radio
        #            button is changed after the fact because we
        #            are referencing myAreResultsTvLinks, rather
        #            than the radio button itself.
        self.updateStatus("Finding seasons. Please wait...")
        if self.myAreResultsTvLinks:
            self.myLinkSite = TVLinks(url)
        else:
            self.myLinkSite = OneChannel(url)
        seasonUpdateMethod = lambda data: self.updateListWidget(data, self.ui.mySeasonListWidget)
        self.createWebRequestThread(seasonUpdateMethod, self.myLinkSite.getSeasons, listWidget=self.ui.mySeasonListWidget)

    def handleChoseSeason(self):
        item = self.getFirstSelectedItem(self.ui.mySeasonListWidget)
        print "selected season %s" % (item.text())
        if item:
            self.ui.mySavePushButton.setEnabled(False)
            self.ui.myWatchPushButton.setEnabled(False)
            self.mySeasonChosen = int(item.text())
            self.updateEpisodes()

    def updateEpisodes(self):
        episodes = self.myLinkSite.getEpisodes(self.mySeasonChosen)
        episodeNames = self.myLinkSite.getEpisodeNames(self.mySeasonChosen)
        self.ui.myEpisodeListWidget.clear()
        for i in range(len(episodes)):
            if episodeNames:
                self.ui.myEpisodeListWidget.addItem("%d : %s" % (episodes[i], episodeNames[i]))
            else:
                self.ui.myEpisodeListWidget.addItem("%d" % (episodes[i]))
            #using setAccessibleDescription as a place to store the episode number because can't find something cleaner.
            self.ui.myEpisodeListWidget.item(i).setStatusTip(str(episodes[i]))
        self.updateStatus("Please select an episode to watch...")

    def handleChoseEpisode(self):
        item = self.getFirstSelectedItem(self.ui.myEpisodeListWidget)
        if item:
            self.myEpisodeChosen = int(item.statusTip())
            self.ui.mySavePushButton.setEnabled(True)
            self.ui.myWatchPushButton.setEnabled(True)
            self.createWebRequestThread(self.updateSummary, self.myLinkSite.getSummary, self.mySeasonChosen, self.myEpisodeChosen, textBrowser=self.ui.mySummaryTextBrowser)

    def updateSummary(self, summary):
        self.ui.mySummaryTextBrowser.setText(summary)

    def handleSave(self):
        self.createWebRequestThread(self.doSave, hostsitepicker.pickFromLinkSite, self.myLinkSite, self.mySeasonChosen, self.myEpisodeChosen)

    def doSave(self, hostSite):
        if hostSite:
            metadata = hostSite.getMetadata()
            videoURL = hostSite.getVideo()
            filename = "%sS%sE%s.%s" % (
                self.myQuery, str(self.mySeasonChosen).zfill(2), str(self.myEpisodeChosen).zfill(2),
                metadata["extension"])
            filename = str(QtGui.QFileDialog.getSaveFileName(self, "Save File", "./" + filename))
            #            processs, status = downloadmanager.startDownloads([(videoURL, filename)])
            # self.myDownloadThread = self.createDownloadThread(videoURL, filename)
            self.pc.addFile(videoURL,filename)
        else:
            self.updateStatus("Couldn't pick a host site. Try a different link site.")

    def handleOpen(self):
        self.createWebRequestThread(self.doOpen, hostsitepicker.pickFromLinkSite, self.myLinkSite, self.mySeasonChosen, self.myEpisodeChosen)

    def doOpen(self, hostSite):
        if hostSite:
            metadata = hostSite.getMetadata()
            videoURL = hostSite.getVideo()
            filename = "%sS%sE%s.%s" % (
                self.myQuery, str(self.mySeasonChosen).zfill(2), str(self.myEpisodeChosen).zfill(2),
                metadata["extension"])
            #            processs, status = downloadmanager.startDownloads([(videoURL, filename)])
            # self.myDownloadThread = self.createDownloadThread(videoURL, filename)
            self.pc.addFile(videoURL,filename)
            self.myFilename = filename
            self.waitForFile(filename)
            #opens arbitrary file in a platform-independent way. 
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', filename))
            elif os.name == 'nt':
            #                os.startfile(filename) #@UndefinedVariable
                #alternatively, we could probably call:
                subprocess.call(('start', filename))
            elif os.name == 'posix':
                subprocess.call(('xdg-open', filename))
        else:
            self.updateStatus("Couldn't pick a host site. Try a different link site.")

    def waitForFile(self, filename):
        assert isinstance(filename, str)

        self.updateStatus("Waiting for file to start downloading...")
        for _ in range(50):
            if os.path.isfile(filename):
                break
            else:
                time.sleep(.2)

    def closeEvent(self, event):
        self.updateStatus("Exiting...")
        if self.myDownloadThread:
            self.myDownloadThread.terminate()
        if self.myFilename and os.path.isfile(self.myFilename):
            os.remove(self.myFilename)
        event.accept()




class WebRequestThread(QtCore.QThread):
    def __init__(self, parent, method, *args):
        QtCore.QThread.__init__(self, parent)
        self.updateListSignal = QtCore.SIGNAL("updateListSignal")
        self.methodToCall = method
        self.args = args

    def run(self):
        listReturned = self.methodToCall(*self.args)
        self.emit(self.updateListSignal, listReturned)


def main():
    app = QtGui.QApplication(sys.argv)
    Form = JankflixForm()
    Form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

