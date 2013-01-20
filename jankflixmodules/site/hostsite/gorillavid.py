from BeautifulSoup import BeautifulSoup
from jankflixmodules.site.template import HostSite
from jankflixmodules.utils import stringutils
from jankflixmodules.utils.decorators import unicodeToAscii, memoized
import urlparse

class Gorillavid(HostSite):
    '''
    Host site implementation of gorillavid.com and gorillavid.in
    '''
    @staticmethod
    def getName():
        return "gorillavid"
    @unicodeToAscii
    def getMetadata(self):
        ret = dict()
        soup = self.getStep2()
        scripts = soup.findAll("script")
        for script in scripts:
            scriptText = script.getText()
            #makes sure it's the right script (there are multiple)
            if len(scriptText) > 0 and scriptText.count('var player = null;') > 0:
                namepart = stringutils.get_after(scriptText, 'file: "')
                ret["name"] = stringutils.get_before(namepart, '"')
                ret["extension"] = ret["name"][-3:]
                durpart = stringutils.get_after(scriptText, 'duration:"')
                ret["duration"] = stringutils.get_before(durpart, '"')
                heightpart = stringutils.get_after(scriptText, 'height: "')
                ret["height"] = stringutils.get_before(heightpart, '"')
                widthpart = stringutils.get_after(scriptText, 'width: "')
                ret["width"] = stringutils.get_before(widthpart, '"')
                imagepart = stringutils.get_after(scriptText, 'image: "')
                ret["image"] = stringutils.get_before(imagepart, '"')
        return ret
    
    @unicodeToAscii
    def getVideo(self):
        newsoup = self.getStep2()
        scripts = newsoup.find("div", {"id":"player_code"}).findAll("script")
        targetScriptText = scripts[2].getText()
        targetScriptPart = stringutils.get_after(targetScriptText, 'file: "')
        targetScriptPart = stringutils.get_before(targetScriptPart, '",')
        return targetScriptPart

    @memoized
    def getStep2(self):
        filename = self.soup.find("input", {"name":"fname", "type":"hidden"}).get("value")
        parse_result = urlparse.urlparse(self.url)
        path = parse_result.path
        key = path.replace("/","")
        postparams = {
            "op":"download1",
            "usr_login":"",
            "id":key,
            "fname":filename,
            "referer":"",
            "channel":self.url.split("/")[3],
            "method_free":"Free Download",
            
        }
        return BeautifulSoup(self.getPage(self.url, postparams))
    
class Movpod(Gorillavid):
    '''
    Host site implementation of movpod.net and movpod.in
    '''
    @staticmethod
    def getName():
        return "movpod"

class Daclips(Gorillavid):
    '''
    Host site implementation of daclips.com and daclips.in
    '''
    @staticmethod
    def getName():
        return "daclips"

