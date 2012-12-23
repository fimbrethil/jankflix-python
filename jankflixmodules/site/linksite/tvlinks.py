from BeautifulSoup import BeautifulSoup
from jankflixmodules.site.linksite.onechannel import OneChannel
from jankflixmodules.site.template import LinkSite
from jankflixmodules.utils.decorators import unicodeToAscii, memoized
import urllib2

class TVLinks(LinkSite):
    '''
    LinkSite implementation of TVLinks.eu
    '''
    
    def getSeasons(self):
        seasons = []
        last_season = self.soup.find("div", "bg_imp biggest bold dark clear").getText()
        seasons.append(str(last_season[7:]))
        for r in self.soup.findAll("div", "bg_imp biggest bold dark clear mt_1"):
            season_num = int(r.getText()[7:8])
            seasons.append(season_num)
        return seasons

    
    def getEpisodes(self, season):
        episodes = self.soup.find("ul", id = "ul_snr" + str(season)).findAll("span", "c1")
        return [int(ep.getText()[8:]) for ep in episodes]
    
    @unicodeToAscii
    def getEpisodeNames(self, season):
        episodes = self.soup.find("ul", id = "ul_snr" + str(season)).findAll("span", "c2")
        return [ep.getText() for ep in episodes]

    @memoized
    def getEpisodeSoup(self, season, episode):
        return BeautifulSoup(self.getPage(self.url + "season_" + str(season) + "/episode_" + str(episode) + "/"))
    
    @memoized
    def getEpisodeResultSoup(self, season, episode):
        return BeautifulSoup(self.getPage(self.url + "season_" + str(season) + "/episode_" + str(episode) + "/video-results/"))
   
    @unicodeToAscii
    def getSummary(self, season, episode):
        episode_soup = self.getEpisodeSoup(season, episode)
        first_part = episode_soup.find("li", "cfix mb_1")
        return first_part.getText()

    @unicodeToAscii
    def getHostSiteTypes(self, season, episode):
        hostTypes = self.getEpisodeResultSoup(season, episode).find("ul", id = "table_search").findAll("span", "block mb_05 nowrap")
        return [host.find("span", "dark").find("span", "bold").getText() for host in hostTypes[3:]]

    @unicodeToAscii
    def getHostSiteAtIndex(self, season, episode, ind):
        resultSoup = self.getEpisodeResultSoup(season, episode)
        epElements = resultSoup.find("ul", id = "table_search").findAll("li")
        gateLinks = [el.find("a").get("onclick")[18:38] for el in epElements]
        url = "http://www.tv-links.eu/gateway.php?data=" + gateLinks[ind + 3]
        request = urllib2.Request(url, None, self.values)
        response = urllib2.urlopen(request)
        return response.geturl()

    @staticmethod
    def searchSite(query):
        surl = "http://www.tv-links.eu/_search/?s=" + query
        resultSoup = BeautifulSoup(OneChannel.getPage(surl))
        titles = [str(res.getText()) for res in resultSoup.findAll("span", "biggest bold")]
        links = [str(res.get("href")) for res in resultSoup.findAll("a", "outer list cfix")]
        tlTuples = []
        for i in range(len(titles)):
            tlTuples.append((titles[i], "http://www.tv-links.eu" + links[i]))
        return tlTuples
