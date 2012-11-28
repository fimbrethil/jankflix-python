'''
Created on Nov 26, 2012

@author: christian
'''
from BeautifulSoup import BeautifulSoup
from hostsite import HostSite
from utils import getBefore, getAfter




class PutLocker(HostSite):
    '''
    classdocs
    '''
    def getBaseUrl(self):
        return "http://www.putlocker.com"

    def getVideo(self):
        hash = self.soup.find("input", {"name":"hash"}).get("value")
        params = {"hash":hash,
                  "confirm":"Please+wait+for+0+seconds"}
        newsoup = BeautifulSoup(self.getPage(self.url, params))
        script = newsoup.find("div", id = "play").find("script").getText()
        script = getAfter(script, "playlist: '")
        script = getBefore(script, "',")

        xmlsoup = BeautifulSoup(self.getPage(self.getBaseUrl() + script))
        return xmlsoup.find("media:content").get("url")

class SockShare(PutLocker):
    '''
    classdocs
    '''
    def getBaseUrl(self):
        return "http://www.sockshare.com"

#pl = PutLocker("http://www.putlocker.com/file/68EFFD1A55851B94")
#pl = SockShare("http://www.sockshare.com/file/2CF81A42124B7657")
#print pl.getVideo()
