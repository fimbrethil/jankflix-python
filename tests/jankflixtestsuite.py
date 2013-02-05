import hostsitetest
import linksitetest
import unittest

def generateTests():
    tests = []
    tests.extend(hostsitetest.generateTests())
    tests.extend(linksitetest.generateTests())
    return tests
if __name__ == "__main__":
    suite = unittest.TestSuite()
    for test in generateTests():
        suite.addTest(test)    
    unittest.TextTestRunner(verbosity = 2).run(suite)