import sys

sys.path.append("..")
from jankflixmodules.utils import constants
#tell Site that we are using the cache
constants.USING_CACHE = True
from jankflixmodules.site.linksite.tvlinks import TVLinks
from jankflixmodules.site import hostsitepicker
from jankflixmodules.site.linksite.onechannel import OneChannel
import unittest


class TestHostSitePicker():
    def setUp(self):
        print "Testing url in sitetest:", self.getLinkSite()

    def getLinkSite(self):
        return self.link_site

    def testIsSupportedHostSite(self):
        self.assertTrue(hostsitepicker.isSupportedHostSite("putlocker"), "putlocker is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("movreel"), "movreel is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("gorillavid"), "gorillavid is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("daclips"), "daclips is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("movpod"), "movpod is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("filebox"), "filebox is supported hostsite")
        self.assertTrue(hostsitepicker.isSupportedHostSite("filenuke"), "filenuke is supported hostsite")

    def testPickFromHostSiteTypes(self):
        #picking arbitrary season, episode
        hostsitepicker.pickFromLinkSite(self.getLinkSite(), 2, 2)


class OneChannelPickingTest(unittest.TestCase, TestHostSitePicker):
    link_site = OneChannel("http://www.1channel.ch/watch-9583-Avatar-The-Last-Airbender")


class TVLinkslPickingTest(unittest.TestCase, TestHostSitePicker):
    link_site = TVLinks("http://www.tv-links.eu/tv-shows/Avatar--The-Last-Airbender_76/")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(OneChannelPickingTest())
    suite.addTest(TVLinkslPickingTest())
    unittest.TextTestRunner(verbosity=2).run(suite)
