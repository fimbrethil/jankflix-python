'''
Created on Nov 26, 2012

@author: christian
'''
from utils.memoization import memoized
from BeautifulSoup import BeautifulSoup
from hostsite import HostSite
from utils.utils import getAfter, getBefore




class PutLocker(HostSite):
    '''
    classdocs
    '''
    def getBaseUrl(self):
        return "http://www.putlocker.com"
    def getName(self):
        return "putlocker"
    def getMetadata(self):
        ret = dict()
        
        soup = self.getNextStep()
        h1 = soup.find("div",{"class":"site-content"}).h1
        ret["name"] = h1.getText()
        ret["size"] = h1.strong.getText()
        ret["extension"] = "flv"
        return ret
    @memoized
    def getNextStep(self):
        hash = self.soup.find("input", {"name":"hash"}).get("value")
        params = {"hash":hash,
                  "confirm":"Please+wait+for+0+seconds"}
        return BeautifulSoup(self.getPage(self.url, params))
    def getVideo(self):
        newsoup = self.getNextStep()
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
    def getName(self):
        return "sockshare"
#pl = PutLocker("http://www.putlocker.com/file/68EFFD1A55851B94")
#pl = SockShare("http://www.sockshare.com/file/2CF81A42124B7657")
#print pl.getVideo()
