from PyQt4 import QtCore, QtGui
from gui_gen import Ui_Form
from jankflixmodules.site import hostsitepicker
from jankflixmodules.site.linksite.onechannel import OneChannel
from jankflixmodules.site.linksite.tvlinks import TVLinks
from jankflixmodules.utils.constants import USER_AGENT
import os
import subprocess
import sys
import time
import urllib2

class JankflixForm(QtGui.QWidget):
    def __init__(self, parent = None):
        super(JankflixForm, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.mySearchLineEdit.returnPressed.connect(self.handleRunQuery)
        self.ui.my1ChannelRadioButton.clicked.connect(lambda:self.handleRadioButton("1channel"))
        self.ui.myTVLinksRadioButton.clicked.connect(lambda:self.handleRadioButton("tvlinks"))
        self.ui.myResultsListView.clicked.connect(self.handleChoseResult)
        self.ui.mySeasonListView.clicked.connect(self.handleChoseSeason)
        self.ui.myEpisodeListView.clicked.connect(self.handleChoseEpisode)
        self.ui.mySavePushButton.clicked.connect(self.handleSave)
        self.ui.myWatchPushButton.clicked.connect(self.handleOpen)
        self.myDownloadThread = None
        self.myWebRequestThread = None
        self.myFilename = None
        self.myFilename = None
        if self.ui.myTVLinksRadioButton.isChecked():
            self.myAreResultsTvLinks = True
        else:
            self.myAreResultsTvLinks = False
    def createDownloadThread(self, url, path):
        workThread = WorkThread(self, url, path)
        self.connect(workThread, workThread.statusSignal, self.ui.myStatusLabel.setText)
        self.connect(workThread, workThread.progressSignal, self.ui.myProgressBar.setValue)
        workThread.start()
        self.ui.myCancelPushButton.setEnabled(True)
        self.ui.myCancelPushButton.clicked.connect(workThread.terminate)
        return workThread
    def createWebRequestThread(self, updateMethod, httpMethod, *args):
        if self.myWebRequestThread != None:
            self.myWebRequestThread.terminate()
        wrThread = WebRequestThread(self, httpMethod, *args)
        self.connect(wrThread, wrThread.updateListSignal, updateMethod)
        self.myWebRequestThread = wrThread
        wrThread.start()


    def updateSearchResults(self, runQueryResult):
        data = [name_url[0] for name_url in runQueryResult]
        self.updateListView(data, self.ui.myResultsListView)
        self.myQueryResult = runQueryResult
        #if there is only one result, automatically select it. 
        if len(data) == 1:
            index = self.ui.myResultsListView.model().index(0,0);
            self.ui.myResultsListView.setCurrentIndex(index)
            self.handleChoseResult()
    def updateListView(self, data, listView):
        model = QtGui.QStandardItemModel()
        for datum in data:
            item = QtGui.QStandardItem(str(datum))
            model.appendRow(item)
        listView.setModel(model)
    def updateStatus(self, status):
        self.ui.myStatusLabel.setText(status)
    def getFirstSelectedIndex(self, listview):
        assert isinstance(listview , QtGui.QListView)
        indecies = listview.selectedIndexes()
        if len(indecies) > 0:
            #gets the row of the selected value
            resultIndex = indecies[0].row()
            return resultIndex
    def getFirstSelectedItem(self, listview):
        index = self.getFirstSelectedIndex(listview)
        print "first selected index returns %d" % (index)
        if index != None:
            model = listview.model()
            item = model.item(index)
            return item


    def handleRadioButton(self, whichButton):
            self.ui.myResultsListView.setModel(QtGui.QStandardItemModel())
            self.ui.mySeasonListView.setModel(QtGui.QStandardItemModel())
            self.ui.myEpisodeListView.setModel(QtGui.QStandardItemModel())
            self.ui.mySavePushButton.setEnabled(False)
            self.ui.myWatchPushButton.setEnabled(False)
            if whichButton == "tvlinks":
                self.myAreResultsTvLinks = True
            else:
                self.myAreResultsTvLinks = False
    def handleRunQuery(self):
        self.myQuery = str(self.ui.mySearchLineEdit.text())
        if len(self.myQuery) > 0:
            self.ui.myResultsListView.setModel(QtGui.QStandardItemModel())
            self.ui.mySeasonListView.setModel(QtGui.QStandardItemModel())
            self.ui.myEpisodeListView.setModel(QtGui.QStandardItemModel())
            self.ui.mySavePushButton.setEnabled(False)
            self.ui.myWatchPushButton.setEnabled(False)
            #create result depending on which linksite was checked
            if self.myAreResultsTvLinks:
                self.updateStatus("Searching TVLinks for %s" % (self.myQuery))
                self.createWebRequestThread(self.updateSearchResults, TVLinks.searchSite, self.myQuery)
            else:
                self.updateStatus("Searching OneChannel for %s" % (self.myQuery))
                self.createWebRequestThread(self.updateSearchResults, OneChannel.searchSite, self.myQuery)
    def handleChoseResult(self):
        index = self.getFirstSelectedIndex(self.ui.myResultsListView)
        if index == None:
            return
        self.ui.mySeasonListView.setModel(QtGui.QStandardItemModel())
        self.ui.myEpisodeListView.setModel(QtGui.QStandardItemModel())
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
        seasonUpdateMethod = lambda data:self.updateListView(data, self.ui.mySeasonListView)
        self.createWebRequestThread(seasonUpdateMethod, self.myLinkSite.getSeasons)

    def handleChoseSeason(self):
        item = self.getFirstSelectedItem(self.ui.mySeasonListView)
        print "selected season %s" % (item.text())
        if item:
            self.ui.myEpisodeListView.setModel(QtGui.QStandardItemModel())
            self.ui.mySavePushButton.setEnabled(False)
            self.ui.myWatchPushButton.setEnabled(False)
            self.mySeasonChosen = item.text()
            self.updateEpisodes()

    def updateEpisodes(self):
        episodes = self.myLinkSite.getEpisodes(self.mySeasonChosen)
        episodeNames = self.myLinkSite.getEpisodeNames(self.mySeasonChosen)
        episodesModel = QtGui.QStandardItemModel()
        for i in range(len(episodes)):
            if episodeNames:
                item = QtGui.QStandardItem("%d : %s" % (episodes[i], episodeNames[i]))
            else:
                item = QtGui.QStandardItem("%d" % (episodes[i]))
            #using setAccessibleDescription as a place to store the episode number because I can't think of a cleaner way. 
            item.setAccessibleDescription(str(episodes[i]))
            episodesModel.appendRow(item)
        self.ui.myEpisodeListView.setModel(episodesModel)
        self.updateStatus("Please select an episode to watch...")

    def handleChoseEpisode(self):
        item = self.getFirstSelectedItem(self.ui.myEpisodeListView)
        if item:
            self.myEpisodeChosen = str(item.accessibleDescription())
            self.ui.mySavePushButton.setEnabled(True)
            self.ui.myWatchPushButton.setEnabled(True)

    def handleSave(self):
        hostSite = hostsitepicker.pickFromLinkSite(self.myLinkSite, self.mySeasonChosen, self.myEpisodeChosen)
        if hostSite:
            metadata = hostSite.getMetadata()
            videoURL = hostSite.getVideo()
            filename = "%sS%sE%s.%s" % (self.myQuery, str(self.mySeasonChosen).zfill(2), str(self.myEpisodeChosen).zfill(2), metadata["extension"])
            filename = str(QtGui.QFileDialog.getSaveFileName(self, "Save File", "./" + filename))
#            processs, status = downloadmanager.startDownloads([(videoURL, filename)])
            self.myDownloadThread = self.createDownloadThread(videoURL, filename)
        else:
            self.updateStatus("Couldn't pick a host site. Try a different link site.")


    def handleOpen(self):
        hostSite = hostsitepicker.pickFromLinkSite(self.myLinkSite, self.mySeasonChosen, self.myEpisodeChosen)
        if hostSite:
            metadata = hostSite.getMetadata()
            videoURL = hostSite.getVideo()
            filename = "%sS%sE%s.%s" % (self.myQuery, str(self.mySeasonChosen).zfill(2), str(self.myEpisodeChosen).zfill(2), metadata["extension"])
#            processs, status = downloadmanager.startDownloads([(videoURL, filename)])
            self.myDownloadThread = self.createDownloadThread(videoURL, filename)
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
class WorkThread(QtCore.QThread):
    def __init__(self, parent, url, path, block_size = 8192):
        QtCore.QThread.__init__(self, parent)
        self.statusSignal = QtCore.SIGNAL("statusSignal")
        self.progressSignal = QtCore.SIGNAL("progressSignal")
        self.url = url
        self.path = path
        self.block_size = block_size
    def run(self):
        print "in thread"
        self.downloadFile(self.url, self.path, self.block_size)
    def downloadFile(self, url, path, block_size = 8192):
        file_name = path.split('/')[-1]
        values = {'User-Agent' : USER_AGENT}
        request = urllib2.Request(url, None, values)
        response = urllib2.urlopen(request)
        f = open(path, 'wb')
        meta = response.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        status = "Downloading: %s Bytes: %s" % (file_name, file_size)
        self.emit(self.statusSignal, status)
        file_size_dl = 0
        while True:
            buf = response.read(block_size)
            if not buf:
                break

            file_size_dl += len(buf)
            f.write(buf)
            status = "%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            self.emit(self.statusSignal, status)
            self.emit(self.progressSignal, file_size_dl * 100. / file_size)
        self.emit(self.statusSignal, "done")
        f.close()



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

