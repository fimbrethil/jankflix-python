'''
Created on Nov 27, 2012

@author: christian
'''
import unittest


class HostSiteTest():
    '''
    classdocs
    '''
    def stateTest(self):
        self.failUnless(self.hs.url in self.hs.getBaseUrl())
    def getVideoTest(self):
        assert isinstance(self, unittest.TestCase)
        video = self.hs

#    def getBaseUrlTest(self):

#class GorillaVidTest(HostSiteTest, unittest.TestCase):
#    @classmethod
#    def setUpClass(cls):
#        cls.hs = GorillaVid("http://gorillavid.com/5jmfrah9alxt")
#        print "in " + cls.__name__ + " passed " + str(stack()[0][3])


#if __name__ == "__main__":
#    #import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
