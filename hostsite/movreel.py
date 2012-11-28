'''
Created on Nov 26, 2012

@author: christian
'''
from BeautifulSoup import BeautifulSoup
from hostsite import HostSite

class MovReel(HostSite):
    '''
    classdocs
    '''
    def getBaseUrl(self):
        return "http://www.movreel.com/"

    def getVideo(self):
        filename = self.soup.find("input", {"name":"fname", "type":"hidden" }).get("value")
        key = self.url.split("/")[3]
        print filename, key
        postparams = {"op":"download1",
                      "usr_login":"",
                      "id":key,
                      "fname":filename,
                      "referer":"",
                      "channel":"cnb",
                      "method_free":"Free Download"}

        newsoup = BeautifulSoup(self.getPage(self.url, postparams))
        rand = newsoup.find("input", {"name":"rand", "type":"hidden"}).get("value")
        postparams = {"op":"download2",
                      "id":key,
                      "rand":rand,
                      "method_free":"Free Download",
                      "method_premium":"",
                      "down_direct":1}

        newsoup = BeautifulSoup(self.getPage(self.url, postparams))
        print newsoup
        return newsoup.find("div", id = "divxshowboxt").find("a").get("href")

#mr = MovReel("http://movreel.com/vm4txj1i7m3w")
#print mr.getVideo()
