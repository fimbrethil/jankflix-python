'''
Created on Nov 26, 2012

@author: christian
'''
from linksite import LinkSite
from utils import getAfter, getBefore
import urllib2
from BeautifulSoup import BeautifulSoup

class OneChannel(LinkSite):
    '''
    classdocs
    '''
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
        ret = []
        for part, souppart in self.getSEParts():
            if part[1] not in ret:
                ret.append(str(part[1]))
        return ret

    def getEpisodes(self, season):
        ret = []
        for part, souppart in self.getSEParts():
            if part[1] == str(season):
                ret.append(str(part[3]))
        return ret

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
        return str(response.geturl())

    @staticmethod
    def searchSite(query):
        surl = "http://www.1channel.ch/index.php"
        soup = BeautifulSoup(OneChannel.getPage(surl))

        key = soup.find("input", {"type":"hidden", "name":"key"}).get("value")
        surl = "http://www.1channel.ch/index.php?search_keywords=" + query + "&key=" + key + "&search_section=2"
        resultSoup = BeautifulSoup(OneChannel.getPage(surl))
        ret = []

        results = resultSoup.findAll("div", {"class":"index_item index_item_ie"})
        for result in results:
            a = result.find("a")
            ret.append((str(a.get("title")), str(a.get("href"))))
        return ret

