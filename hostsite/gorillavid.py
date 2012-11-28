'''
Created on Nov 26, 2012

@author: christian
'''
from BeautifulSoup import BeautifulSoup
from utils import getAfter, getBefore
from hostsite import HostSite
class GorillaVid(HostSite):
    '''
    classdocs
    '''
    def getBaseUrl(self):
        return "http://www.gorillavid.in"

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
        return script

class MovPod(GorillaVid):
    '''
    classdocs
    '''
    def getBaseUrl(self):
        return "http://www.movpod.in"

class DaClipz(GorillaVid):
    '''
    classdocs
    '''
    def getBaseUrl(self):
        return "http://www.daclips.com"
#gv = GorillaVid("http://gorillavid.com/5jmfrah9alxt")
#gv = DaClipz("http://daclips.in/q31wexpl2omp")
#gv = MovPod("http://movpod.in/aly8yr7jfw6f")
#print gv.getVideo()
