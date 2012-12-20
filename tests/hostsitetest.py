'''
Created on Nov 27, 2012

@author: christian
'''
import unittest
from inspect import stack
from linksite.tvlinks import TVLinks
from linksite import linksite
from hostsite.hostsite import HostSite

class TestManyHostSites(unittest.TestCase):
    @classmethod
    
    def setUpClass(cls):
        search = TVLinks.searchSite("avatar")
        l = None
        for name, link in search:
            if "Airbender" in name :
                l = link
        print l
        cls.tl = TVLinks(l)
        print "in " + cls.__name__ + " passed " + str(stack()[0][3])
    def testManyHostSites(self):
        season = 3
        episode = 9
        sites = self.tl.getHostSiteTypes(season, episode)
        for i in range(len(sites)):
            site = sites[i]
            for hs in linksite.supportedSites:
                if hs.getName() in site:
                    linksite.supportedSites.remove(hs)
                    hostsiteurl = self.tl.getHostSiteAtIndex(season, episode, i)
                    assert isinstance(hs, HostSite)
                    hs.__init__(hostsiteurl)
                    print hs.getMetadata()
                    print hs.getVideo()
                    print "got video for " + hs.getName()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
