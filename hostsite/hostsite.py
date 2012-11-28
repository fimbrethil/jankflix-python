'''
Created on Nov 26, 2012

@author: christian
'''
from site import Site

class HostSite(Site):
    '''
    classdocs
    '''
    def getVideo(self):
        raise NotImplementedError
    def getBaseUrl(self):
        raise NotImplementedError
    