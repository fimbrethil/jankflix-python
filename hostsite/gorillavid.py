'''
Created on Nov 26, 2012

@author: christian
'''
from utils import memoization
from utils.memoization import memoized
__all__ = ["GorillaVid", "MovPod", "DaClipz"]
from BeautifulSoup import BeautifulSoup
from hostsite import HostSite
from utils.utils import getAfter, getBefore

class GorillaVid(HostSite):
    '''
    classdocs
    '''
    def getName(self):
        return "gorillavid"
    def getMetadata(self):
        ret = dict()
        soup = self.getStep2()
        scripts = soup.findAll("script")
        for script in scripts:
            text = script.getText()
            if len(text) > 0 and text.count('var player = null;') >0:
                namepart = getAfter(text, 'file: "')
                ret["name"] = getBefore(namepart, '"')
                ret["extension"] = ret["name"][-3:]
                durpart = getAfter(text, 'duration:"')
                ret["duration"] = getBefore(durpart, '"')
                heightpart = getAfter(text, 'height: "')
                ret["height"] = getBefore(heightpart, '"')
                widthpart = getAfter(text, 'width: "')
                ret["width"] = getBefore(widthpart, '"')
                imagepart = getAfter(text, 'image: "')
                ret["image"] = getBefore(imagepart, '"')
        return ret
    def getVideo(self):
        newsoup = self.getStep2()
        script = newsoup.find("div", {"id":"player_code"})

        script = script.findAll("script")
        script = script[2].getText()
        script = getAfter(script, 'file: "')
        script = getBefore(script, '",')
        return str(script)
    
    @memoized
    def getStep2(self):
        filename = self.soup.find("input", {"name":"fname", "type":"hidden"}).get("value")
        key = self.url.split("/")[3]
        postparams = {"op":"download1",
                      "usr_login":"",
                      "id":key,
                      "fname":filename,
                      "referer":"",
                      "method_free":"Free Download"}
        return BeautifulSoup(self.getPage(self.url, postparams))
class MovPod(GorillaVid):
    '''
    classdocs
    '''
    def getName(self):
        return "movpod"

class DaClipz(GorillaVid):
    '''
    classdocs
    '''
    def getName(self):
        return "daclips"
#gv = GorillaVid("http://gorillavid.com/5jmfrah9alxt")
#gv = DaClipz("http://daclips.in/q31wexpl2omp")
#gv = MovPod("http://movpod.in/aly8yr7jfw6f")
#print gv.getVideo()
