import unittest
import urlparse
from parameterizedtestcase import ParametrizedTestCase
from jankflixmodules.site.hostsite.putlocker import Sockshare, Putlocker
from jankflixmodules.site.hostsite.movreel import Movreel
from jankflixmodules.site.hostsite.gorillavid import Gorillavid, Daclips, Movpod
from jankflixmodules.site.hostsite.filebox import FileBox
from jankflixmodules.site.hostsite.filenuke import FileNuke
class TestHostSite(ParametrizedTestCase):

    def testGetVideo(self):
        video = self.param.getVideo()
        print video
        self.assertIsInstance(video, str, type(video))

    def testGetName(self):
        name = self.param.getName()
        self.assertIsInstance(name, str, type(name))
        self.assertIn(name, self.param.url, "%s in %s" % (name, self.param.url))

    def testGetMetadata(self):
        metadata = self.param.getMetadata()
        self.assertIsInstance(metadata, dict, type(metadata))
        self.assertIn("extension", metadata.keys(), metadata["extension"])

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(TestHostSite, param=Sockshare("http://www.sockshare.com/file/0A09CBFA173FCFFA")))
    suite.addTest(ParametrizedTestCase.parametrize(TestHostSite, param = Putlocker("http://www.putlocker.com/file/68EFFD1A55851B94")))
    suite.addTest(ParametrizedTestCase.parametrize(TestHostSite, param=Movreel("http://movreel.com/vm4txj1i7m3w")))
    suite.addTest(ParametrizedTestCase.parametrize(TestHostSite, param = Gorillavid("http://gorillavid.in/v1jy9v47gq4x")))
    suite.addTest(ParametrizedTestCase.parametrize(TestHostSite, param = Gorillavid("http://gorillavid.in/n0ph9afqgr0k")))
    suite.addTest(ParametrizedTestCase.parametrize(TestHostSite, param = Daclips("http://daclips.in/q31wexpl2omp")))
    suite.addTest(ParametrizedTestCase.parametrize(TestHostSite, param = Movpod("http://movpod.in/aly8yr7jfw6f")))
    suite.addTest(ParametrizedTestCase.parametrize(TestHostSite, param = FileBox("http://www.filebox.com/pv78hy1iqqem")))
    suite.addTest(ParametrizedTestCase.parametrize(TestHostSite, param = FileNuke("http://filenuke.com/3b6c44atsjky")))
    unittest.TextTestRunner(verbosity = 2).run(suite)
