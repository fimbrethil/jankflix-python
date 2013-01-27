from BeautifulSoup import BeautifulSoup
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
        time_to_sleep = self.soup.find("span",id="countdown_str").find("span").getText()
        time.sleep(int(time_to_sleep))
        form = self.soup.find("form", {"name":"F1","method":"POST"})
        op = form.find("input", {"name":"op","type":"hidden"}).get("value")
        id = form.find("input", {"name":"id","type":"hidden"}).get("value")
        rand = form.find("input", {"name":"rand", "type":"hidden"}).get("value")
        referer = form.find("input", {"name":"referer", "type":"hidden"}).get("value")
        method_free = form.find("input", {"name":"method_free", "type":"hidden"}).get("value")
        method_premium = form.find("input", {"name":"method_premium", "type":"hidden"}).get("value")
        down_direct = form.find("input", {"name":"down_direct", "type":"hidden"}).get("value")
        postparams = {
            "op":op,
            "id":id,
            "rand":rand,
            "referer":referer,
            "method_free":method_free,
            "method_premium":method_premium,
            "down_direct":down_direct,
        }
        return BeautifulSoup(self.getPage(self.url, postparams))

