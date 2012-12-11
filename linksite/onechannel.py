'''
Created on Nov 26, 2012

@author: christian
'''
from linksite import LinkSite
import urllib2
from BeautifulSoup import BeautifulSoup
from utils.utils import getAfter, getBefore
import urlparse
from utils.memoization import memoized
import urllib

class OneChannel(LinkSite):
    '''
    classdocs
    '''
    @memoized
    def getSEParts(self):
        items = self.soup.findAll("div", {"class":"tv_episode_item"})
        ret = []
        for item in items:

            link = item.find("a").get("href")
            parts = link.split("/")
            things = parts[len(parts) - 1].split("-")
            ret.append((things, item))
        return ret

    def getSeasons(self):
        seasons = []
        for part, souppart in self.getSEParts():
            if part[1] not in seasons:
                seasons.append(str(part[1]))
        intSeasons = [int(season) for season in seasons]
        return intSeasons

    def getEpisodes(self, season):
        episodes = []
        for part, souppart in self.getSEParts():
            if part[1] == str(season):
                episodes.append(str(part[3]))
        intEpisodes = [int(episode) for episode in episodes]
        return intEpisodes

    def getEpisodeNames(self, season):
        ret = []
        for part, souppart in self.getSEParts():
            if part[1] == str(season):
                ret.append(str(souppart.find("a").find("span").getText()))
        return ret

    def getEpisodeURL(self, season, episode):
        for part, souppart in self.getSEParts():
            if part[1] == str(season) and part[3] == str(episode):
                return "http://www.1channel.ch" + str(souppart.find("a").get("href"))

    def getEpisodeSoup(self, season, episode):
        return BeautifulSoup(OneChannel.getPage(self.getEpisodeURL(season, episode)))

    def getSummary(self, season, episode):
        soup = self.getEpisodeSoup(season, episode)
        return str(soup.find("p", style = "width:460px; display:block;").getText()).strip()

    def getHostSiteTypes(self, season, episode):
        sites = self.getEpisodeSoup(season, episode).findAll("span", {"class":"version_host"})
        types = []
        for site in sites:
            site = str(site.getText())
            site = getAfter(site, "('")
            site = getBefore(site, "')")
            types.append(site)
        return types

    def getHostSiteAtIndex(self, season, episode, index):
        soup = BeautifulSoup(OneChannel.getPage(self.getEpisodeURL(season, episode)))
        links = soup.findAll("span", {"class":"movie_version_link"})
        url = "http://www.1channel.ch" + links[index].find("a").get("href")
        request = urllib2.Request(url, None, self.values)
        response = urllib2.urlopen(request)
        parseresult = urlparse.urlparse(response.geturl())
        if parseresult.hostname == "www.1channel.ch":
            res = str(response.read())
            response.close()
            res = res.replace("iso-8859-1", "utf-8")
            nextSoup = BeautifulSoup(res)
            return nextSoup.findAll("frame")[1].get("src")
        return str(response.geturl())

    @staticmethod
    def searchSite(query):
        surl = "http://www.1channel.ch/index.php"
        soup = BeautifulSoup(OneChannel.getPage(surl))
        key = soup.find("input", {"type":"hidden", "name":"key"}).get("value")
        params = {"search_keywords":query,
                  "key":key,
                  "search_section":"2"}
        surl = "http://www.1channel.ch/index.php?"+urllib.urlencode(params)
        resultSoup = BeautifulSoup(OneChannel.getPage(surl))
        ret = []

        results = resultSoup.findAll("div", {"class":"index_item index_item_ie"})
        for result in results:
            a = result.find("a")
            ret.append((str(a.get("title")), "http://www.1channel.ch" + str(a.get("href"))))
        return ret

