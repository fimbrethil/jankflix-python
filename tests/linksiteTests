'''
Created on Nov 27, 2012

@author: christian
'''
import unittest
from linksite.tvlinks import TVLinks
from inspect import stack
from linksite.onechannel import OneChannel

class BaseLinkSiteTest():

    def testGetSeasons(self):
        self.failIf(len(self.tl.getSeasons()) != 3)
        print "in " + self.__class__.__name__ + " passed " + str(stack()[0][3])
    def testGetEpisodes(self):
        self.failIf(len(self.tl.getEpisodes(2)) != 20)
        print "in " + self.__class__.__name__ + " passed " + str(stack()[0][3])
    def testEpisodeNames(self):
        epNames = self.tl.getEpisodeNames(2)
        self.failIf(len(epNames) != 20)
        self.failUnless("Desert" in epNames[10])
        print "in " + self.__class__.__name__ + " passed " + str(stack()[0][3])
    def testSummary(self):
        summ = self.tl.getSummary(2, 10)
        self.failUnless(type(summ) is str)
        self.failIf(len(summ) < 10)
        print "in " + self.__class__.__name__ + " passed " + str(stack()[0][3])
    def testHostSiteTypes(self):
        types = self.tl.getHostSiteTypes(2, 10)
        self.failUnless(type(types) is list)
        self.failUnless(len(types) > 1)
        print "in " + self.__class__.__name__ + " passed " + str(stack()[0][3])
    def testHostSiteAtIndex(self):
        types = self.tl.getHostSiteTypes(2, 10)
        siteAtIndex = self.tl.getHostSiteAtIndex(2, 10, 1)
        self.failUnless(type(siteAtIndex) is str)
        print types[1]
        print siteAtIndex
        self.failUnless(types[1] in siteAtIndex)
        print "in " + self.__class__.__name__ + " passed " + str(stack()[0][3])

class OneChannelTest(BaseLinkSiteTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        search = OneChannel.searchSite("avatar")
        l = None
        for name, link in search:
            if "Airbender" in name :
                l = link
#        cls.failIf(l == None)
        cls.tl = OneChannel("http://1channel.ch" + l)
        print "in " + cls.__name__ + " passed " + str(stack()[0][3])

class TVLinksTest(BaseLinkSiteTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        search = TVLinks.searchSite("avatar")
        l = None
        for name, link in search:
            if name == "Avatar: The Last Airbender":
                l = link
#        cls.failIf(l == None)
        cls.tl = TVLinks("http://www.tv-links.eu" + l)
        print "in " + cls.__name__ + " passed " + str(stack()[0][3])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'BaseTest.testTVLinks']
    unittest.main()
