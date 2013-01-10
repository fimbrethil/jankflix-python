from jankflixmodules.utils.constants import USER_AGENT
import multiprocessing
import site
import urllib2
def startDownloads(urlPathPairs):
    '''
    Starts multiple downloads given many urls to download from and corresponding local paths to download to. 
    @param urlPathPairs: a list of (url to download from, path to save to)
    @type urlPathPairs: a list of (str, str) 
    @return: (list of all processes started, list of statuses coming from each process) (the ith process maps to the ith status)
    @rtype: (list of multiprocessing.Process, list of multiprocessing.Queue of strings)
    '''
    processs = []
    status = []
    for url,path in urlPathPairs:
        mystatus = multiprocessing.Queue()
        process = multiprocessing.Process(target = download, args = [url,path,mystatus,8192*4])
        process.start()
        status.append(mystatus)
        processs.append(process)
    return processs,status

def download(url,path,status,block_size = 8192):
    file_name = path.split('/')[-1]
    values = {'User-Agent' : USER_AGENT}
    request = urllib2.Request(url, None, values)
    response = urllib2.urlopen(request)
    f = open(path, 'wb')
    meta = response.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    status.put("Downloading: %s Bytes: %s" % (file_name, file_size))
    file_size_dl = 0
    while True:
        buf = response.read(block_size)
        if not buf:
            break

        file_size_dl += len(buf)
        f.write(buf)
        status.put(r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size))
    status.put("done")
    f.close()
    

