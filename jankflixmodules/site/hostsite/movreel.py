from BeautifulSoup import BeautifulSoup
from jankflixmodules.site.template import HostSite
from jankflixmodules.utils import stringutils
from jankflixmodules.utils.decorators import memoized, unicodeToAscii

__all__ = ["Movreel"]


class Movreel(HostSite):
    '''
    Host site implementation of movreel.com
    '''
    @staticmethod
    def getName():
        return "movreel"
    @unicodeToAscii
    def getMetadata(self):
        soup = self.getNextStep()
        scripts = soup.find("div", id = "divxshowboxt").findAll("script")
        ret = dict()
        for script in scripts:
            text = script.getText()
            if len(text) > 0 and text.count("var file_name = escape('") > 0:
                namepart = stringutils.get_after(text, "var file_name = escape('")
                ret["name"] = stringutils.get_before(namepart, "');\n")
                ret["extension"] = ret["name"][-3:]

        return ret
    
    @memoized
    def getNextStep(self):
        form = self.soup.find("form", method="POST")
        extra = form.find("input", type="submit")
        extra_tuple = (str(extra.get("name")), str(extra.get("value")))
        newsoup = self.submitPostRequest(form, extra_tuple)
        form = newsoup.find("form", {"name":"F1","method":"POST"})
        return self.submitPostRequest(form)
    @unicodeToAscii
    def getVideo(self):
        newsoup = self.getNextStep()
        return newsoup.find("div", id = "divxshowboxt").find("a").get("href")
