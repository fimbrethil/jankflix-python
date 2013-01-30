from BeautifulSoup import BeautifulSoup, Tag
from jankflixmodules.utils.constants import USER_AGENT
import urllib
import urllib2


class Site(object):
    '''
    Generic class for all site objects. 
    '''
    def __init__(self, url = None):
        if url != None:
            page, newUrl = Site.getPageWithRedirectedURL(url)
            self.soup = BeautifulSoup(page)
            self.url = newUrl
            self.values = {'User-Agent' : USER_AGENT}
    @staticmethod
    def getPage(url, postParams = None):
        values = {'User-Agent' : USER_AGENT}
        if postParams == None:
            request = urllib2.Request(url, postParams, values)
        else:
            print "requesting with params:",str(urllib.urlencode(postParams))
            request = urllib2.Request(url, urllib.urlencode(postParams), values)
        response = urllib2.urlopen(request)
        res = str(response.read())
        response.close()
        res = res.replace("iso-8859-1", "utf-8")
        return res
    @staticmethod
    def getPageWithRedirectedURL(url, postParams = None):
        values = {'User-Agent' : USER_AGENT}
        if postParams == None:
            request = urllib2.Request(url, postParams, values)
        else:
            request = urllib2.Request(url, urllib.urlencode(postParams), values)
        response = urllib2.urlopen(request)
        res = str(response.read())
        redirected = response.geturl()
        
        response.close()
        res = res.replace("iso-8859-1", "utf-8")
        return (res, redirected)
    def submitPostRequest(self, formSoup, extra = None):
        assert isinstance(formSoup, Tag)
        if extra:
            assert isinstance(extra, tuple) 
            assert len(extra) == 2
            assert isinstance(extra[0], str)
            assert isinstance(extra[1], str)
        inputs = formSoup.findAll("input", type="hidden")
        if extra:
            postparams = dict([extra])
        else:
            postparams = dict()
        for input in inputs:
            name = str(input.get("name"))
            value = str(input.get("value"))
            print name,value
            postparams[name] = value
        
        return BeautifulSoup(self.getPage(self.url, postparams))


class HostSite(Site):
    '''
    Template for host site implementations with method signatures that must be implemented. 
    '''
    def getVideo(self):
        '''
        @return: URL at which the target video is located
        @rtype: string
        '''
        raise NotImplementedError
    
    @staticmethod
    def getName():
        '''
        @return: A string that identifies the website and one which will return true if site_url contains rval is called.
        @rtype: string
        '''
        raise NotImplementedError
    
    def getMetadata(self):
        '''
        @return: A dictionary with all the metadata directly available on the website. (video size, length, quality, etc.)
        Keys currently in use on one or more host site implementations are:
        extension
        summary
        size
        views
        video_info
        audio_info
        name
        extension
        duration
        height
        width
        image
        @rtype: dict
        '''
        return NotImplementedError

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
        @return: A list of episode names, or none if no names exist. 
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
    
    @staticmethod
    def searchSite(self, query):
        '''
        @param query: String to search for
        @return: List of results which contains a human-readable portion and a full URL to the episode page. 
        @rtype: List of tuples. The first element is the human-readable string. The second is the URL. 
        '''
        raise NotImplementedError
    
   
