import sys
sys.path.append("..")
import unittest
from jankflixmodules.site.hostsite.gorillavid import Gorillavid, Daclips, Movpod
from jankflixmodules.site.hostsite.movreel import Movreel
from jankflixmodules.site.hostsite.putlocker import Sockshare, Putlocker
from tests.parameterizedtestcase import ParametrizedTestCase
from jankflixmodules.site.hostsite.filenuke import FileNuke
from jankflixmodules.site.hostsite.filebox import FileBox


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

def generateTests():
    tests = []
    tests.append(ParametrizedTestCase.parametrize(TestHostSite, param = Sockshare("http://www.sockshare.com/file/0A09CBFA173FCFFA")))
    tests.append(ParametrizedTestCase.parametrize(TestHostSite, param = Putlocker("http://www.putlocker.com/file/68EFFD1A55851B94")))

    tests.append(ParametrizedTestCase.parametrize(TestHostSite, param = Movreel("http://movreel.com/vm4txj1i7m3w")))

    tests.append(ParametrizedTestCase.parametrize(TestHostSite, param = Gorillavid("http://gorillavid.in/v1jy9v47gq4x")))
    tests.append(ParametrizedTestCase.parametrize(TestHostSite, param = Gorillavid("http://gorillavid.in/n0ph9afqgr0k")))
    tests.append(ParametrizedTestCase.parametrize(TestHostSite, param = Daclips("http://daclips.in/wdl6vubb3nde")))
    tests.append(ParametrizedTestCase.parametrize(TestHostSite, param = Movpod("http://movpod.in/aly8yr7jfw6f")))

    tests.append(ParametrizedTestCase.parametrize(TestHostSite, param = FileBox("http://www.filebox.com/pv78hy1iqqem")))

    tests.append(ParametrizedTestCase.parametrize(TestHostSite, param = FileNuke("http://filenuke.com/3b6c44atsjky")))
    return tests
if __name__ == "__main__":
    suite = unittest.TestSuite()
    for test in generateTests():
        suite.addTest(test)    
    unittest.TextTestRunner(verbosity = 2).run(suite)
