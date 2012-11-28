'''
Created on Nov 27, 2012

@author: christian
'''
import unittest
from hostsite.gorillavid import GorillaVid
from inspect import stack


class HostSiteTest():

    def testGetVideo(self):
        video = self.hs.getVideo()
        self.failUnless(type(video) is str)
        print video
    def testGetBaseUrl(self):
        print self.hs.url, self.hs.getBaseUrl()
        self.failUnless(self.hs.url in self.hs.getBaseUrl())

class GorillaVidTest(HostSiteTest, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hs = GorillaVid("http://gorillavid.com/5jmfrah9alxt")
        print "in " + cls.__name__ + " passed " + str(stack()[0][3])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
