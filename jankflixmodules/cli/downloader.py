from PyQt4 import QtGui, QtCore
import urllib2
from jankflixmodules.utils.constants import USER_AGENT


class ProgressCancel:
    def __init__(self, parent, myProgressCancelVerticalLayout):
        self.progressBars = []
        self.cancelButtons = []
        self.workThreads = []
        self.myProgressCancelVerticalLayout = myProgressCancelVerticalLayout
        self.parent = parent

    def addFile(self, url, path):
        currentIndex = len(self.cancelButtons)
        [progress, cancel] = self.addDownloadProgressAndButton()
        workThread = self.addDownloadThread(url, path, currentIndex)
        #update internal state
        self.progressBars.append(progress)
        self.cancelButtons.append(cancel)
        self.workThreads.append(workThread)
        #set cancel click callback to call appropriate handler
        cancel.clicked.connect(lambda: self.handleCancelClicked(currentIndex))
        #set progress callback from ith workthread to ith progress bar
        setCurrProgressValue = lambda (value): self.setProgressValue(currentIndex, value)
        self.parent.connect(workThread, workThread.progressSignal, setCurrProgressValue)

    def addDownloadThread(self, url, path, index):
        assert isinstance(url, str)
        assert isinstance(path, str)

        workThread = WorkThread(self.parent, url, path)
        # self.connect(workThread, workThread.statusSignal, self.ui.myStatusLabel.setText)
        workThread.start()
        return workThread

    def addDownloadProgressAndButton(self):
        myHorizontalLayout = QtGui.QHBoxLayout()
        myProgressBar = QtGui.QProgressBar(self.parent)
        myProgressBar.setEnabled(False)
        myProgressBar.setProperty("value", 0)
        myHorizontalLayout.addWidget(myProgressBar)
        myCancelButton = QtGui.QPushButton(self.parent)
        myCancelButton.setText("Cancel")
        myHorizontalLayout.addWidget(myCancelButton)
        self.myProgressCancelVerticalLayout.addLayout(myHorizontalLayout)
        return [myProgressBar, myCancelButton]

    def handleCancelClicked(self, index):
        print index, "clicked"
        self.workThreads[index].terminate()
        self.progressBars[index].hide()
        self.cancelButtons[index].hide()

    def setProgressValue(self, index, value):
        self.progressBars[index].setValue(value)


class WorkThread(QtCore.QThread):
    def __init__(self, parent, url, path, block_size=8192):
        QtCore.QThread.__init__(self, parent)
        self.statusSignal = QtCore.SIGNAL("statusSignal")
        self.progressSignal = QtCore.SIGNAL("progressSignal")
        self.url = url
        self.path = path
        self.block_size = block_size

    def run(self):
        print "in thread"
        self.downloadFile(self.url, self.path, self.block_size)

    def downloadFile(self, url, path, block_size=8192):
        file_name = path.split('/')[-1]
        values = {'User-Agent': USER_AGENT}
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
