'''
Created on Nov 27, 2012

@author: christian
'''
import unittest
from hostsite.gorillavid import GorillaVid
from inspect import stack
from linksite.tvlinks import TVLinks
from linksite.onechannel import OneChannel
from linksite import linksite
from linksite.linksite import LinkSite
from hostsite.hostsite import HostSite
#class HostSiteTest():
#
#    def testGetVideo(self):
#
#        video = self.hs.getVideo()
#        print type(video)
#        self.failUnless(type(video) is str)
#        print video
#    def testGetBaseUrl(self):
#        print self.hs.url, self.hs.getBaseUrl()
#        self.failUnless(self.hs.getBaseUrl() in self.hs.url)
#
#class GorillaVidTest(HostSiteTest, unittest.TestCase):
#    @classmethod
#    def setUpClass(cls):
#        cls.hs = GorillaVid("http://gorillavid.com/5jmfrah9alxt")
#        print "in " + cls.__name__ + " passed " + str(stack()[0][3])

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
