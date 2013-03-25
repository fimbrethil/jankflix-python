from jankflixmodules.site.template import HostSite
from jankflixmodules.utils.decorators import unicodeToAscii, memoized
from jankflixmodules.utils import stringutils
from jankflixmodules.utils.stringutils import get_after, get_before

class FileNuke(HostSite):
    '''
    Host site implementation of filenuke
    '''
    @staticmethod
    def getName():
        return "filenuke"
    @unicodeToAscii
    def getMetadata(self):
        soup = self.getStep2()
        all_blocks = soup.find("div", id="header-block2")
        all_rows = all_blocks.findAll("div",{"class":"fileinfo-row"})
        
        text_to_key_mapping = { "Description:":"summary",
                               "Size:":"size",
                               "Downloaded:":"views",
                               "Length:":"duration",
                               "Video info:":"video_info",
                               "Audio info:":"audio_info",
                               }
        metadata = dict()
        for row in all_rows:
            
            text = row.find("span","label").getText()
            value = row.find(text=True,recursive=False)
            key = text_to_key_mapping[text]
            metadata[key] = value
        video = self.getVideo()
        metadata["extension"] = video.split(".")[-1]
        return metadata
            
    
    @unicodeToAscii
    def getVideo(self):
        newsoup = self.getStep2()
        scripts = newsoup.findAll("script")
        for script in scripts:
            text = script.getText()
            if text[0:4] == "eval" and "SWFObject" in text:
                script = stringutils.decode_packed_javascript(text)
                after = get_after(script, "addVariable('file','")
                middle = get_before(after,"');")
                return middle

    @memoized
    def getStep2(self):
        form = self.getSoup().find("tr")
        method_free = form.find("input", {"name":"method_free"})
        name = str(method_free.get("name"))
        value = str(method_free.get("value"))
        return self.submitPostRequest(form, (name,value))

