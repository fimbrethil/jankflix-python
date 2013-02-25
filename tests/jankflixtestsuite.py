import sys
sys.path.append("..")
from jankflixmodules.utils import constants
#tell Site that we are using the cache
constants.USING_CACHE = True
import hostsitetest
import linksitetest
import sitetest
import unittest


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTests()
    unittest.TextTestRunner(verbosity = 2).run(suite)