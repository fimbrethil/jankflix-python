from jankflixmodules.site.template import HostSite
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
        return target_div.find("a").get("href")

    @memoized
    def getStep2(self):
        time_to_sleep = self.getSoup().find("span",id="countdown_str").find("span").getText()
        time.sleep(int(time_to_sleep))
        form = self.getSoup().find("form", {"name":"F1","method":"POST"})
        return self.submitPostRequest(form)

