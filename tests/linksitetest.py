import unittest
import urlparse
from jankflixmodules.site.linksite.tvlinks import TVLinks
from jankflixmodules.site.linksite.onechannel import OneChannel
from parameterizedtestcase import ParametrizedTestCase
class TestLinkSite(ParametrizedTestCase):
    
    def testGetSeasons(self):
        seasons = self.param.getSeasons()
        self.assertIsInstance(seasons, list, type(seasons))
        self.assertGreater(len(seasons), 0, len(seasons))
        for season in seasons:
            self.assertIsInstance(season,int,type(season))
   
    def testGetEpisodes(self):
        seasons = self.param.getSeasons()
        for season in seasons:
            episodes = self.param.getEpisodes(season)
            self.assertIsInstance(episodes, list, type(episodes))
            self.assertGreater(len(episodes), 0, len(episodes))
            for episode in episodes:
                self.assertIsInstance(episode,int,type(episode))
    
    def testGetEpisodeNames(self):
        seasons = self.param.getSeasons()
        for season in seasons:
            episode_names = self.param.getEpisodeNames(season)
            self.assertIsInstance(episode_names, list, type(episode_names))
            for episode_name in episode_names:
                self.assertIsInstance(episode_name, str,type(episode_name))
                self.assertGreater(len(episode_name), 0,len(episode_name))
    def testGetSummary(self):
        seasons = self.param.getSeasons()
        for season in seasons:
            episodes = self.param.getEpisodes(season)
            #this is done for speed considerations, so one doesn't need to
            #make O(n) web calls where n is the number of total episodes
            summary = self.param.getSummary(season,episodes[0])
            self.assertIsInstance(summary,str,type(summary))
            self.assertGreater(len(summary), 0,len(summary))
    def testGetHostSiteTypes(self):
        
        seasons = self.param.getSeasons()
        for season in seasons:
            episodes = self.param.getEpisodes(season)
            #this is done for speed considerations, so one doesn't need to
            #make O(n) web calls where n is the number of total episodes
            host_site_types = self.param.getHostSiteTypes(season, episodes[0])
            for host_site_type in host_site_types:
                self.assertIsInstance(host_site_type,str,type(host_site_type))
                self.assertGreater(len(host_site_type), 0,len(host_site_type))
            
            
    
    def testGetHostSiteAtIndex(self):
        #because many link sites are rate-limited on the number of host-sites
        #we will only resolve 1 host site. 
        #While this is not an exhaustive test, it balances actually testing
        #part of the method with running into rate limits on resolutions. 
        
        #pick the first season
        season = self.param.getSeasons()[0]
        #pick the first episode
        episode = self.param.getEpisodes(season)[0]
        host_site_types = self.param.getHostSiteTypes(season,episode)
        #get the (0) index of the last host site
        index = len(host_site_types)-1
        #attempt to resolve it to a host site url
        host_site = self.param.getHostSiteAtIndex(season,episode,index)
        self.assertIsInstance(host_site,str,type(host_site))
        self.assertGreater(len(host_site), 0,len(host_site))
        
        
        '''
        @param season: Season of the host site types to get
        @param episode: Episode of the host site types to get
        @param index: Index of the host site to resolve
        @return: URL of the host site at the given index in the page
        @rtype: string
        '''
   
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(TestLinkSite, param=OneChannel("http://www.1channel.ch/watch-9583-Avatar-The-Last-Airbender")))
    suite.addTest(ParametrizedTestCase.parametrize(TestLinkSite, param=TVLinks("http://www.tv-links.eu/tv-shows/Avatar--The-Last-Airbender_76/")))
    unittest.TextTestRunner(verbosity=2).run(suite)
