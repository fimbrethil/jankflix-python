'''
Created on Nov 26, 2012

@author: christian
'''
__all__ = ["HostSite"]
from utils.site import Site

class HostSite(Site):
    '''
    classdocs
    '''
    def getVideo(self):
        '''
        @return: URL at which the target video is located
        @rtype: string
        '''
        raise NotImplementedError
    def getName(self):
        '''
        @return: A string that identifies the website and one which will return true if site_url contains rval is called.
        @rtype: string
        '''
        raise NotImplementedError
    def getMetadata(self):
        '''
        @return: A dictionary with all the metadata directly available on the website. (video size, length, quality, etc.)
        @rtype: dict
        '''
        