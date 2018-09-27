#coding=utf-8
import argparse
import os

import mslogger

"""
an encapsulation for argparse
"""

class MSArgParser(object):
    """
    the implementation
    """
    def __init__(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--config", default="./spider.conf", dest="configfile", help="indicate the config file")
        parser.add_argument("-v", "--version", action="version", version="version 0.0.0", help="show the version")
        self.__args = parser.parse_args(argv)
        self.__logger = mslogger.MSLogger()

    def getConfigFile(self):
        """
        get the config file, absolute path
        """
        if not self.__args.configfile:
            msg = "not set configfile"
            self.__logger.error(msg)
            return ""
        cf = os.getcwd() + os.sep + self.__args.configfile
        if not os.path.exists(self.__args.configfile):
            msg = "file " + cf + " not exist!"
            self.__logger.error(msg)
            return ""
        return cf

if __name__ == "__main__":
    testargv = ['-c', 'test/spider.config']
    msarg = MSArgParser(testargv)
    print(msarg.getConfigFile())
    print(os.getcwd())
    print( os.path.exists(os.getcwd() + '/test/spider.config'))