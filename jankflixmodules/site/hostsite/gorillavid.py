from BeautifulSoup import BeautifulSoup
from jankflixmodules.site.template import HostSite
from jankflixmodules.utils import stringutils
from jankflixmodules.utils.decorators import unicodeToAscii, memoized

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
                namepart = stringutils.getAfter(scriptText, 'file: "')
                ret["name"] = stringutils.getBefore(namepart, '"')
                ret["extension"] = ret["name"][-3:]
                durpart = stringutils.getAfter(scriptText, 'duration:"')
                ret["duration"] = stringutils.getBefore(durpart, '"')
                heightpart = stringutils.getAfter(scriptText, 'height: "')
                ret["height"] = stringutils.getBefore(heightpart, '"')
                widthpart = stringutils.getAfter(scriptText, 'width: "')
                ret["width"] = stringutils.getBefore(widthpart, '"')
                imagepart = stringutils.getAfter(scriptText, 'image: "')
                ret["image"] = stringutils.getBefore(imagepart, '"')
        return ret
    
    @unicodeToAscii
    def getVideo(self):
        newsoup = self.getStep2()
        scripts = newsoup.find("div", {"id":"player_code"}).findAll("script")
        targetScriptText = scripts[2].getText()
        targetScriptPart = stringutils.getAfter(targetScriptText, 'file: "')
        targetScriptPart = stringutils.getBefore(targetScriptPart, '",')
        return targetScriptPart

    @memoized
    def getStep2(self):
        filename = self.soup.find("input", {"name":"fname", "type":"hidden"}).get("value")
        key = self.url.split("/")[4]
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

