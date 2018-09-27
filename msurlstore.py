#-*- coding: UTF-8 -*-
import os

import mslogger

class MSUrlStore(object):
    
    def _read_seed_file(self):
        """read the contents in seedfile to unvistedUrls"""
        try:
            if not os.path.exists(self.__seedfile):
                self.__logger.error("seedfile:" + self.__seedfile + " not exist!")
                return
            with open(self.__seedfile, "r") as file:
                for line in file.readlines():
                    self.pushUrl(line.strip())
        except IOError as e:
            self.__logger.error(e)
        else:
            self.__logger.info("use seedfile:" + self.__seedfile)

    def __init__(self, seedfile):
        """the invoker should make sure the seedfile is exist"""
        # the file which have the seed sites
        self.__seedfile = seedfile
        # the unvisite sites
        self.__unvistedUrls = []
        # the visited sites
        self.__visitedUrls = []
        self.__logger = mslogger.MSLogger()
        self._read_seed_file()

    def popUrl(self):
        """
        get one unvisited url, not thread safe
        """
        url = ""
        if len(self.__unvistedUrls) > 0:
            url = self.__unvistedUrls[0]
            self.__unvistedUrls = self.__unvistedUrls[1:]
        return url

    def pushUrl(self, url):
        """
        add one unvisited url, not thread safe
        check url is valid or not??
        """
        if not self.checkVisitedUrl(url):
            self.__unvistedUrls.append(url)
            return True
        return False

    def pushVisitedUrl(self, url):
        """
        add the visited url to visitedUrls
        """
        if not self.checkVisitedUrl(url):
            self.__visitedUrls.append(url)
            return True
        return False

    def checkVisitedUrl(self, url):
        """
        check if the url in visitedUrls
        """
        return url in self.__visitedUrls

if __name__ == "__main__":
    seedfile = "test/urls.txt"
    seedfile_path = os.getcwd() + os.sep + seedfile
    msurlstore = MSUrlStore(seedfile_path)

    url = msurlstore.popUrl()
    print(url.strip())
    msurlstore.pushVisitedUrl(url)
    print(msurlstore.checkVisitedUrl(url))
    url = msurlstore.popUrl()
    print(url, msurlstore.checkVisitedUrl(url))
    url = msurlstore.popUrl()
    print("url:" , url, msurlstore.checkVisitedUrl(url))
    print(msurlstore.pushUrl("http://baidu.com"))
    print(msurlstore.pushUrl("http://www.baidu.com"))
    url = msurlstore.popUrl()
    print(url.strip())
    url = msurlstore.popUrl()
    print("url:", url.strip())
