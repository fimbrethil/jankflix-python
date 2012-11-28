'''
Created on Nov 26, 2012

@author: christian
'''
import urllib2
from site import Site
from BeautifulSoup import BeautifulSoup
from linksite import LinkSite

class TVLinks(LinkSite):
    '''
    classdocs
    '''




    def getSeasons(self):
        ret = []
        lastSeason = self.soup.find("div", "bg_imp biggest bold dark clear").getText()
        ret.append(str(lastSeason[7:]))
        for r in self.soup.findAll("div", "bg_imp biggest bold dark clear mt_1"):
            ret.append(str(r.getText()[7:8]))
        return ret

    def getEpisodes(self, season):
        episodes = self.soup.find("ul", id = "ul_snr" + str(season)).findAll("span", "c1")
        return [str(ep.getText()[8:]) for ep in episodes]

    def getEpisodeNames(self, season):
        episodes = self.soup.find("ul", id = "ul_snr" + str(season)).findAll("span", "c2")
        return [str(ep.getText()) for ep in episodes]

    def getEpisodeURL(self, season, episode):
        return BeautifulSoup(self.getPage(self.url + "season_" + str(season) + "/episode_" + str(episode) + "/"))

    def getResultSoup(self, season, episode):
        return BeautifulSoup(self.getPage(self.url + "season_" + str(season) + "/episode_" + str(episode) + "/video-results/"))

    def getSummary(self, season, episode):
        epSoup = self.getEpisodeURL(season, episode)
        firstPart = epSoup.find("li", "cfix mb_1")
        return str(firstPart.getText())

    def getHostSiteTypes(self, season, episode):
        hostTypes = self.getResultSoup(season, episode).find("ul", id = "table_search").findAll("span", "block mb_05 nowrap")
        return [str(host.find("span", "dark").find("span", "bold").getText()) for host in hostTypes[3:]]

    def getHostSiteAtIndex(self, season, episode, ind):
        resultSoup = self.getResultSoup(season, episode)
        epElements = resultSoup.find("ul", id = "table_search").findAll("li")
        gateLinks = [el.find("a").get("onclick")[18:38] for el in epElements]
        url = "http://www.tv-links.eu/gateway.php?data=" + gateLinks[ind + 3]
        request = urllib2.Request(url, None, self.values)
        response = urllib2.urlopen(request)
        return str(response.geturl())

    @staticmethod
    def searchSite(query):
        surl = "http://www.tv-links.eu/_search/?s=" + query
        resultSoup = BeautifulSoup(Site.getPage(surl))
        titles = [str(res.getText()) for res in resultSoup.findAll("span", "biggest bold")]
        links = [str(res.get("href")) for res in resultSoup.findAll("a", "outer list cfix")]
        tlTuples = []
        for i in range(len(titles)):
            tlTuples.append((titles[i], links[i]))
        return tlTuples



