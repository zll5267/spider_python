#-*- encoding: UTF-8 -*-
import os
import unittest

import mslogger
import msargparser
import msconfigparser

class MSLoggerTestCases(unittest.TestCase):
    def test_same_logger(self):
        """
        singleton test
        """
        myLogger = mslogger.MSLogger()
        myLogger2 = mslogger.MSLogger()
        self.assertEqual(myLogger, myLogger2)

class MSArgParserTestCases(unittest.TestCase):
    def test_get_config_file(self):
        configFile = 'test/spider.config'
        testargv = ['-c', configFile]
        msarg = msargparser.MSArgParser(testargv)
        #print(msarg.getConfigFile())
        self.assertTrue(msarg.getConfigFile().endswith(configFile))

class MSConfigParserTestCases(unittest.TestCase):
    def test_get_config(self):
        cfn = os.getcwd() + os.sep + "test/spider.config"
        msconfig = msconfigparser.MSConfigParser(cfn)
        self.assertEqual(msconfig.crawlInterval, "1")
        self.assertEqual(msconfig.maxDepth, "1")

def suite_use_test_loader():
    """use testLoader
    """
    test_cases = (MSLoggerTestCases,MSArgParserTestCases, MSConfigParserTestCases)
    suite = unittest.TestSuite()
    for test_case in test_cases:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        suite.addTests(tests)
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite_use_test_loader')