from jankflixmodules.site.template import LinkSite
from jankflixmodules.utils.decorators import unicodeToAscii, memoized
from jankflixmodules import utils
import urlparse
from jankflixmodules.utils import stringutils

class TVLinks(LinkSite):
    '''
    LinkSite implementation of TVLinks.eu
    '''
    def __init__(self, url = None):
        if url:
            assert isinstance(url, str)
        scheme, host, path, params, query, fragment =\
            urlparse.urlparse(url)
        if path[-1] != "/":
            path+="/"
            url = urlparse.urlunparse((scheme, host, path, params, query, fragment))
        super(TVLinks, self).__init__(url)

    def getSeasons(self):
        seasons = []
        last_season_dirty = str(self.getSoup().find("div", "bg_imp biggest bold dark clear").getText())
        last_season_dirty = last_season_dirty.replace("- show episodes","")
        last_season = int(last_season_dirty.replace("Season","").strip())
        seasons.append(last_season)
        for r in self.getSoup().findAll("div", "bg_imp biggest bold dark clear mt_1"):
            season_num = int(r.getText()[7:8])
            seasons.append(season_num)
        return sorted(seasons)

    def getEpisodes(self, season):
        assert isinstance(season, int)
        
        episodes = self.getSoup().find("ul", id = "ul_snr" + str(season)).findAll("span", "c1")
        intepisodes =  [int(ep.getText()[8:]) for ep in episodes]
        return sorted(intepisodes)

    @unicodeToAscii
    def getEpisodeNames(self, season):
        assert isinstance(season, int)
        
        try:
            episodes = self.getSoup().find("ul", id = "ul_snr" + str(season)).findAll("span", "c2")
            return [ep.getText() for ep in episodes]
        except:
            return None

    @memoized
    def getEpisodeSoup(self, season, episode):
        assert isinstance(season, int)
        assert isinstance(episode, int)
        return self.getPageSoup(self.url + "season_" + str(season) + "/episode_" + str(episode) + "/")


    @memoized
    def getEpisodeResultSoup(self, season, episode):
        assert isinstance(season, int)
        assert isinstance(episode, int)
        
        return self.getPageSoup(self.url + "season_" + str(season) + "/episode_" + str(episode) + "/video-results/")

    @unicodeToAscii
    def getSummary(self, season, episode):
        assert isinstance(season, int)
        assert isinstance(episode, int)
        
        episode_soup = self.getEpisodeSoup(season, episode)
        first_part = episode_soup.find("li", "cfix mb_1")
        return first_part.getText()

    @unicodeToAscii
    def getHostSiteTypes(self, season, episode):
        assert isinstance(season, int)
        assert isinstance(episode, int)
        
        hostTypes = self.getEpisodeResultSoup(season, episode).find("ul", id = "table_search").findAll("span", "block mb_05 nowrap")
        host_sites_with_visit  = [host.find("span", "bigger bold underline").getText() for host in hostTypes]
        return [host_site.replace("Visit ","") for host_site in host_sites_with_visit]

    @unicodeToAscii
    def getHostSiteAtIndex(self, season, episode, index):
        assert isinstance(season, int)
        assert isinstance(episode, int)
        assert isinstance(index, int)
        
        resultSoup = self.getEpisodeResultSoup(season, episode)
        epElements = resultSoup.find("ul", id = "table_search").findAll("li")
        gateLinks = [el.find("a").get("onclick") for el in epElements]
        targetGateLink = gateLinks[index]
        data = utils.stringutils.get_after(targetGateLink, "frameLink('")
        data = utils.stringutils.get_before(data, "');")
        url = "http://www.tv-links.eu/gateway.php?data=" + data
        return self.getPageSoup(url).url

    @staticmethod
    def searchSite(query):
        assert isinstance(query, str)
        
        surl = "http://www.tv-links.eu/_search/?s=" + query
        resultSoup = TVLinks.getPageSoup(surl)
        
        tlTuples = []
        for search_result in resultSoup.findAll("a","outer list cfix"):
            meta_data = search_result.find("span","block x3")
            category = None
            for span in meta_data.findAll("span","dark"):
                if("Category" in span.getText()):
                    category = str(span.nextSibling)
            if "TV" in category:
                link = "http://www.tv-links.eu" + search_result.get("href")
                title = search_result.find("span", "biggest bold").getText()
                tlTuples.append((str(title), str(link)))
        return tlTuples
