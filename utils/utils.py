'''
Created on Nov 21, 2012

@author: christian
'''
import urllib2
__all__ = ["getAfter", "getBefore", "download"]
import shutil


'''
classdocs
'''
#supportedSites = [("putlocker", PutLocker),
#                  ("sockshare", SockShare),
#                  ("gorillavid", GorillaVid),
#                  ("movpod", MovPod),
#                  ("daclipz", DaClipz),
#                  ("movreel", MovReel)]

def getAfter(string, afterThis):
        return string[string.index(afterThis) + len(afterThis):]

def getBefore(string, beforeThis):
        return string[:string.index(beforeThis)]
#def pickHostSite(hostSites):
#    sites = self.getHostSiteTypes(season, episode)
#        for i in range(len(sites)):
#            site = sites[i]
#            for name, obj in supportedSites:
#                if name in site:
#                    hostsite = self.getHostSiteAtIndex(season, episode, i)
#                    print name, site, hostsite
#                    obj.setPage(hostsite)
#                    return obj

CHUNK = 16 * 1024
download_go = True
def download(request, path):

    with open(path, 'wb') as fp:
        while download_go:
            chunk = request.read(CHUNK)
            if not chunk: break
            fp.write(chunk)
        fp.close()


#def strToHostsite(url):
