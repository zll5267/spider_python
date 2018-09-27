# -*- coding : UTF-8 -*-

import os
import configparser

import mslogger

"""
and encapsulation for configparser
"""
class MSConfigParser(object):
    def __init__(self, configfile):
        """
        the invoker should make sure the configfile is exists!
        """
        self.__logger = mslogger.MSLogger()
        if not os.path.exists(configfile):
            msg = "file " + configfile + " not exist!"
            self.__logger.error(msg)
            return
        self.__config = configparser.ConfigParser(inline_comment_prefixes=(';'))
        self.__logger.info("configfile:" + configfile)
        self.__config.read(configfile, "utf-8")
        self.__spiderSection = "spider"
        self.__urlListFile = self.getSpiderConfig("url_list_file")
        self.__outputDirectory = self.getSpiderConfig("output_directory")
        self.__maxDepth = self.getSpiderConfig("max_depth")
        self.__crawlInterval = self.getSpiderConfig("crawl_interval")
        self.__crawlTimeout = self.getSpiderConfig("crawl_timeout")
        self.__targetUrl = self.getSpiderConfig("target_url")
        self.__threadCount = self.getSpiderConfig("thread_count")

    def getConfig(self, section, name):
        return self.__config.get(section, name)
    
    def getSpiderConfig(self, name):
        return self.getConfig(self.__spiderSection, name)

    @property
    def urlListFile(self):
        return self.__urlListFile

    @property
    def outputDirectory(self):
        return self.__outputDirectory
    
    @property
    def maxDepth(self):
        return self.__maxDepth
    
    @property
    def crawlInterval(self):
        return self.__crawlInterval

    @property
    def crawlTimeout(self):
        return self.__crawlTimeout

    @property
    def targetUrl(self):
        return self.__targetUrl

    @property
    def threadCount(self):
        return self.__threadCount

if __name__ == '__main__':
    # print os.getcwd()
    cfn = os.getcwd() + os.sep + "test/spider.config"
    # with open(cfn) as f:
    #     print f.read()
    msconfig = MSConfigParser(cfn)
    names = ["url_list_file", "output_directory", "max_depth", "crawl_interval", "crawl_timeout", "target_url", "thread_count"]
    for name in names:
        print(name, ":", msconfig.getSpiderConfig(name))