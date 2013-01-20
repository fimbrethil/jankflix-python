from BeautifulSoup import BeautifulSoup
from jankflixmodules.site.template import HostSite
from jankflixmodules.utils import stringutils
from jankflixmodules.utils.decorators import memoized, unicodeToAscii


class Putlocker(HostSite):
    '''
    Host site implementation of putlocker.com
    '''
    def getBaseUrl(self):
        return "http://www.putlocker.com"
    
    @staticmethod
    def getName():
        return "putlocker"
    @unicodeToAscii
    def getMetadata(self):
        metadata = dict()
        soup = self.getNextStep()
        h1 = soup.find("div",{"class":"site-content"}).h1
        metadata["name"] = h1.getText()
        metadata["size"] = h1.strong.getText()
        metadata["extension"] = "flv"
        return metadata
    
    @memoized
    def getNextStep(self):
        page_hash = self.soup.find("input", {"name":"hash"}).get("value")
        params = {"hash":page_hash,
                  "confirm":"Continue as Free User"}
        return BeautifulSoup(self.getPage(self.url, params))
    @unicodeToAscii
    def getVideo(self):
        newsoup = self.getNextStep()
        script = newsoup.find("div", id = "play").find("script").getText()
        script = stringutils.get_after(script, "playlist: '")
        script = stringutils.get_before(script, "',")

        xmlsoup = BeautifulSoup(self.getPage(self.getBaseUrl() + script))
        return xmlsoup.find("media:content").get("url")

class Sockshare(Putlocker):
    '''
    Host site implementation of sockshare.com
    '''
    def getBaseUrl(self):
        return "http://www.sockshare.com"
    @staticmethod
    def getName():
        return "sockshare"
