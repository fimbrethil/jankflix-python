import sys
sys.path.append("..")
from jankflixmodules.utils import constants
#tell Site that we are using the cache
constants.USING_CACHE = True
import unittest
from jankflixmodules.site.hostsite.gorillavid import Gorillavid, Daclips, Movpod
from jankflixmodules.site.hostsite.movreel import Movreel
from jankflixmodules.site.hostsite.putlocker import Sockshare, Putlocker
from jankflixmodules.site.hostsite.filenuke import FileNuke
from jankflixmodules.site.hostsite.filebox import FileBox


class TestHostSite():
    def getHostSite(self):
        return self.host_site

    def testGetVideo(self):
        video = self.getHostSite().getVideo()
        print video
        self.assertIsInstance(video, str, type(video))

    def testGetName(self):
        name = self.getHostSite().getName()
        self.assertIsInstance(name, str, type(name))
        self.assertIn(name, self.getHostSite().url, "%s in %s" % (name, self.getHostSite().url))

    def testGetMetadata(self):
        metadata = self.getHostSite().getMetadata()
        self.assertIsInstance(metadata, dict, type(metadata))
        self.assertIn("extension", metadata.keys(), metadata["extension"])


class TestSockShare(unittest.TestCase, TestHostSite):
    host_site = Sockshare("http://www.sockshare.com/file/0A09CBFA173FCFFA")


class TestPutlocker(unittest.TestCase, TestHostSite):
    host_site = Putlocker("http://www.putlocker.com/file/68EFFD1A55851B94")


class TestMovreel(unittest.TestCase, TestHostSite):
    host_site = Movreel("http://movreel.com/vm4txj1i7m3w")


class TestGorillavid(unittest.TestCase, TestHostSite):
    host_site = Gorillavid("http://gorillavid.in/v1jy9v47gq4x")


class TestGorillavid2(unittest.TestCase, TestHostSite):
    host_site = Gorillavid("http://gorillavid.in/n0ph9afqgr0k")


class TestDaclips(unittest.TestCase, TestHostSite):
    host_site = Daclips("http://daclips.in/wdl6vubb3nde")


class TestMovpod(unittest.TestCase, TestHostSite):
    host_site = Movpod("http://movpod.in/aly8yr7jfw6f")


class TestFileBox(unittest.TestCase, TestHostSite):
    host_site = FileBox("http://www.filebox.com/pv78hy1iqqem")


class TestFileNuke(unittest.TestCase, TestHostSite):
    host_site = FileNuke("http://filenuke.com/3b6c44atsjky")

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestSockShare())
    suite.addTest(TestPutlocker())
    suite.addTest(TestMovpod())
    suite.addTest(TestGorillavid())
    suite.addTest(TestGorillavid2())
    suite.addTest(TestDaclips())
    suite.addTest(TestMovpod())
    suite.addTest(TestMovreel())
    suite.addTest(TestFileBox())
    suite.addTest(TestFileNuke())
    unittest.TextTestRunner(verbosity=2).run(suite)
