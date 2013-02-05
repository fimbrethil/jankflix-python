from tests.parameterizedtestcase import ParametrizedTestCase
from jankflixmodules.site import hostsitepicker
class TestHostSitePicker(ParametrizedTestCase):

    def testIsSupportedHostSite(self):
        self.assert_(hostsitepicker.isSupportedHostSite("putlocker"),"putlocker is supported hostsite")
        self.assertIsInstance(video, str, type(video))

    
def generateTests():
    tests = []
    tests.append(ParametrizedTestCase.parametrize(TestHostSite, param = None)
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
