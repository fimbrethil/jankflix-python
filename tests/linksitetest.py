import sys
sys.path.append("..")
from jankflixmodules.utils import constants
#tell Site that we are using the cache
constants.USING_CACHE = True
import unittest
from jankflixmodules.site.linksite.tvlinks import TVLinks
from jankflixmodules.site.linksite.onechannel import OneChannel
from jankflixmodules.site.template import LinkSite


class TestLinkSite():

    def getLinkSite(self):
        return self.link_site

    def testGetSeasons(self):
        seasons = self.getLinkSite().getSeasons()
        self.assertIsInstance(seasons, list, type(seasons))
        self.assertGreater(len(seasons), 0, len(seasons))
        #Checks that none of the seasons are the same
        seen = []
        for season in seasons:
            self.assertNotIn(season, seen)
            seen.append(season)
            self.assertIsInstance(season,int,type(season))

    def testGetEpisodes(self):
        seasons = self.getLinkSite().getSeasons()
        for season in seasons:
            episodes = self.getLinkSite().getEpisodes(season)
            self.assertIsInstance(episodes, list, type(episodes))
            self.assertGreater(len(episodes), 0, len(episodes))
            #Checks that none of the episodes are the same
            seen = []
            for episode in episodes:
                self.assertNotIn(episode, seen)
                seen.append(episode)
                self.assertIsInstance(episode,int,type(episode))

    def testGetEpisodeNames(self):
        seasons = self.getLinkSite().getSeasons()
        for season in seasons:
            episode_names = self.getLinkSite().getEpisodeNames(season)
            self.assertIsInstance(episode_names, list, type(episode_names))
            for episode_name in episode_names:
                self.assertIsInstance(episode_name, str,type(episode_name))
                self.assertGreater(len(episode_name), 0,len(episode_name))

    def testGetSummary(self):
        seasons = self.getLinkSite().getSeasons()
        for season in seasons:
            episodes = self.getLinkSite().getEpisodes(season)
            #this is done for speed considerations, so one doesn't need to
            #make O(n) web calls where n is the number of total episodes
            summary = self.getLinkSite().getSummary(season,episodes[0])
            self.assertIsInstance(summary,str,type(summary))
            self.assertGreater(len(summary), 0,len(summary))

    def testGetHostSiteTypes(self):

        seasons = self.getLinkSite().getSeasons()
        for season in seasons:
            episodes = self.getLinkSite().getEpisodes(season)
            #this is done for speed considerations, so one doesn't need to
            #make O(n) web calls where n is the number of total episodes
            host_site_types = self.getLinkSite().getHostSiteTypes(season, episodes[0])
            for host_site_type in host_site_types:
                self.assertIsInstance(host_site_type, str, type(host_site_type))
                self.assertGreater(len(host_site_type), 0, len(host_site_type))

    def testGetHostSiteAtIndex(self):
        #because many link sites are rate-limited on the number of host-sites
        #we will only resolve 1 host site.
        #While this is not an exhaustive test, it balances actually testing
        #part of the method with running into rate limits on resolutions.

        #pick the first season
        season = self.getLinkSite().getSeasons()[0]
        #pick the first episode
        episode = self.getLinkSite().getEpisodes(season)[0]
        #resolve host site types
        host_site_types = self.getLinkSite().getHostSiteTypes(season, episode)
        #get the (0) index of the last host site
        index = len(host_site_types)-1
        #attempt to resolve it to a host site url
        if index >= 0:
            host_site = self.getLinkSite().getHostSiteAtIndex(season,episode,index)
            self.assertIsInstance(host_site,str,type(host_site))
            self.assertGreater(len(host_site), 0,len(host_site))


class TestOneChannel(unittest.TestCase, TestLinkSite):
    link_site = OneChannel("http://www.1channel.ch/watch-9583-Avatar-The-Last-Airbender")


class TestTVLinks(unittest.TestCase, TestLinkSite):
    link_site = TVLinks("http://www.tv-links.eu/tv-shows/Avatar--The-Last-Airbender_76/")


class TestTVLinks2(unittest.TestCase, TestLinkSite):
    link_site = TVLinks("http://www.tv-links.eu/tv-shows/Game-of-Thrones--_25243/")


class TestTVLinks3(unittest.TestCase, TestLinkSite):
    link_site = TVLinks("http://www.tv-links.eu/tv-shows/How-It-s-Made_23839/")



class TestLinkSiteSearch():
    def getLinkSiteClass(self):
        raise NotImplementedError()

    def getQuery(self):
        raise NotImplementedError()

    def testSearchSite(self):
        self.assertTrue(issubclass(self.getLinkSiteClass(), LinkSite))
        self.assertIsInstance(self.getQuery(), str)
        search_result = self.getLinkSiteClass().searchSite(self.getQuery())
        self.assertIsNotNone(search_result)
        self.assertGreater(len(search_result), 0)
        for result in search_result:
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], str)
            self.assertIsInstance(result[1], str)


class TestOneChannelSearch(unittest.TestCase, TestLinkSiteSearch):
    def getLinkSiteClass(self):
        return OneChannel

    def getQuery(self):
        return "avatar"


class TestTVLinksSearch(unittest.TestCase, TestLinkSiteSearch):
    def getLinkSiteClass(self):
        return TVLinks

    def getQuery(self):
        return "avatar"


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestOneChannel)
    suite.addTest(TestTVLinks)
    suite.addTest(TestTVLinks2)
    suite.addTest(TestOneChannelSearch)
    suite.addTest(TestTVLinksSearch)
    unittest.TextTestRunner(verbosity = 2).run(suite)