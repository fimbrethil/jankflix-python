from jankflixmodules.site import hostsitepicker
from jankflixmodules.site.linksite.onechannel import OneChannel
from parameterizedtestcase import ParametrizedTestCase
import unittest
class TestHostSitePicker(ParametrizedTestCase):

    def testIsSupportedHostSite(self):
        self.assertTrue(hostsitepicker.isSupportedHostSite("putlocker"),"putlocker is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("movreel"),"movreel is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("gorillavid"),"gorillavid is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("daclips"),"daclips is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("movpod"),"movpod is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("filebox"),"filebox is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("filenuke"),"filenuke is supported hostsite")
        
    def testPickFromHostSiteTypes(self):
        #picking arbitrary season, episode
        hostsitepicker.pickFromLinkSite(self.param, 2, 2)
    
def generateTests():
    tests = []
    tests.append(ParametrizedTestCase.parametrize(TestHostSitePicker, param = OneChannel("http://www.1channel.ch/watch-9583-Avatar-The-Last-Airbender")))
    
    return tests
if __name__ == "__main__":
    suite = unittest.TestSuite()
    for test in generateTests():
        suite.addTest(test)    
    unittest.TextTestRunner(verbosity = 2).run(suite)
