'''
Created on Nov 20, 2012

@author: christian
'''
from site import Site




class LinkSite(Site):
    '''
    classdocs
    '''


    def getSeasons(self):
        raise NotImplementedError
    def getEpisodes(self, season):
        raise NotImplementedError
    def getEpisodeNames(self, season):
        raise NotImplementedError
    def getSummary(self, season, episode):
        raise NotImplementedError
    def getHostSiteTypes(self, season, episode):
        raise NotImplementedError
    def getHostSiteAtIndex(self, season, episode, index):
        raise NotImplementedError
    def getHostSite(self, season, episode):
        sites = self.getHostSiteTypes(season, episode)
        for i in range(len(sites)):
            site = sites[i]
            if site in self.supportedSites:
                return self.getHostSiteAtIndex(season, episode, i)
    def searchSite(self, query):
        raise NotImplementedError




