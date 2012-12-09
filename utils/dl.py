'''
Created on Doec 7, 2012

@author: christian
'''
import urllib2

import multiprocessing
from site import USER_AGENT

def startDownloads(urlPathPairs):
    processs = []
    status = []
    for url,path in urlPathPairs:
        mystatus = multiprocessing.Queue()
        process = multiprocessing.Process(target = download, args = [url,path,mystatus])
        
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
        buffer = response.read(block_size)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status.put(r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size))
    status.put("done")
    f.close()
    

