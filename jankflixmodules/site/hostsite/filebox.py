from jankflixmodules.site.template import HostSite
from jankflixmodules.utils import stringutils
from jankflixmodules.utils.decorators import unicodeToAscii, memoized
import time

class FileBox(HostSite):
    '''
    Host site implementation of filebox
    '''
    @staticmethod
    def getName():
        return "filebox"
    @unicodeToAscii
    def getMetadata(self):
        ret = dict()
        my_video = self.getVideo()
        extension = my_video.split(".")[-1]
        ret["extension"] = extension
        return ret
    
    @unicodeToAscii
    def getVideo(self):
        newsoup = self.getStep2()
        target_div = newsoup.find("div", {"class":"getpremium_heading4"})
        almost_link = target_div.center.input["onclick"]
        #get after the beginning document.location=' business and remove the last character which is a '
        return stringutils.get_after(almost_link,"document.location='")[:-1]

    @memoized
    def getStep2(self):
        soup = self.getSoup()
        time_to_sleep = soup.find("span", id="countdown_str").find("span").getText()
        if not soup.from_cache:
            print "sleeping for ", time_to_sleep, " seconds"
            time.sleep(int(time_to_sleep))
        form = self.getSoup().find("form", {"name": "F1", "method": "POST"})
        return self.submitPostRequest(form)

