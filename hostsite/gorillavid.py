'''
Created on Nov 26, 2012

@author: christian
'''
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

    def getVideo(self):
        filename = self.soup.find("input", {"name":"fname", "type":"hidden"}).get("value")
        key = self.url.split("/")[3]
        postparams = {"op":"download1",
                      "usr_login":"",
                      "id":key,
                      "fname":filename,
                      "referer":"",
                      "method_free":"Free Download"}
        print filename
        newsoup = BeautifulSoup(self.getPage(self.url, postparams))
#        print newsoup
        script = newsoup.find("div", {"id":"player_code"})

        script = script.findAll("script")
        script = script[2].getText()
        script = getAfter(script, 'file: "')
        script = getBefore(script, '",')
        return str(script)

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
