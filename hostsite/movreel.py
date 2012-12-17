'''
Created on Nov 26, 2012

@author: christian
'''
from utils.memoization import memoized
from utils.utils import getAfter, getBefore
__all__ = ["MovReel"]
from BeautifulSoup import BeautifulSoup
from hostsite import HostSite

class MovReel(HostSite):
    '''
    classdocs
    '''
    def getName(self):
        return "movreel"
    def getMetadata(self):
        soup = self.getNextStep()
        scripts = soup.find("div",id="divxshowboxt").findAll("script")
        ret = dict()
        for script in scripts:
            text = script.getText()
            if len(text) > 0 and text.count("var file_name = escape('") >0:
                namepart = getAfter(text, "var file_name = escape('")
                ret["name"] = getBefore(namepart, "');\n")
                ret["extension"] = ret["name"][-3:]

        return ret
    @memoized
    def getNextStep(self):
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

        return BeautifulSoup(self.getPage(self.url, postparams))
    def getVideo(self):
        
        newsoup = self.getNextStep()
        return newsoup.find("div", id = "divxshowboxt").find("a").get("href")

#mr = MovReel("http://movreel.com/vm4txj1i7m3w")
#print mr.getVideo()
