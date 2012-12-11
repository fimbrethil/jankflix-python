'''
Created on Nov 20, 2012

@author: christian
'''
from utils.site import Site
from hostsite.gorillavid import *
from hostsite.putlocker import *
from hostsite.hostsite import *






supportedSites = [("putlocker", PutLocker()), ("sockshare", SockShare()),
                  ("gorillavid", GorillaVid()),
                  ("movpod", MovPod()),
                  ("daclipz", DaClipz())]



class LinkSite(Site):
    '''
    An abstract class for a specific linksite to implement
    '''


    def getSeasons(self):
        '''
        @return: A list of season numbers
        @rtype: list of ints
        '''
        raise NotImplementedError
    def getEpisodes(self, season):
        '''
        
        @param season: Season for which to get episodes
        @return: A list of episode numbers
        @rtype: list of ints
        '''
        raise NotImplementedError
    def getEpisodeNames(self, season):
        '''
        @param season: Season for which to get episode names
        @return: A list of episode names
        @rtype: list
        '''
        raise NotImplementedError
    def getSummary(self, season, episode):
        '''
        @param season: Season of the summary
        @param episode: Epsiode of the summary
        @return: String of the summary of the episode
        @rtype: string
        '''

        raise NotImplementedError
    def getHostSiteTypes(self, season, episode):
        '''
        
        @param season: Season of the host site types to get
        @param episode: Episode of the host site types to get
        @return: Host sites that this link site provides.
        @rtype: list of strings
        '''
        raise NotImplementedError
    def getHostSiteAtIndex(self, season, episode, index):
        '''
        
        @param season: Season of the host site types to get
        @param episode: Episode of the host site types to get
        @param index: Index of the host site to resolve
        @return: URL of the host site at the given index in the page
        @rtype: string
        '''

        raise NotImplementedError
#    def getHostSite(self, season, episode):
#        sites = self.getHostSiteTypes(season, episode)
#        for i in range(len(sites)):
#            site = sites[i]
#            if site in self.supportedSites:
#                return self.getHostSiteAtIndex(season, episode, i)
    def searchSite(self, query):
        '''
        
        @param query: String to search for
        @return: List of results which contains a human-readable portion and a full URL to the episode page. 
        @rtype: List of tuples. The first element is the human-readable string. The second is the URL. 
        '''

        raise NotImplementedError
    def getHostSite(self, season, episode):
        sites = self.getHostSiteTypes(season, episode)
        for i in range(len(sites)):
            site = sites[i]
            for name, hs in supportedSites:
                if name in site:
                    hostsiteurl = self.getHostSiteAtIndex(season, episode, i)
                    assert isinstance(hs, HostSite)
                    hs.__init__(hostsiteurl)
                    return hs.getVideo()



