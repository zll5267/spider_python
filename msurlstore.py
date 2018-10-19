#-*- coding: UTF-8 -*-
import os
import threading
import queue

import mslogger
import msconfigparser

"""
the element in the queue is a dict
{"url":"http://www.baidu.com", "depth":0}
"""
class MSUrlStore(object):

    def _read_seed_file(self):
        """read the contents in seedfile to unvistedUrls"""
        try:
            if not os.path.exists(self.__seedfile):
                self.__logger.error("seedfile:" + self.__seedfile + " not exist!")
                return
            with open(self.__seedfile, "r") as file:
                for line in file.readlines():
                    url = {"url":line.strip(), "depth":0}
                    self.pushUrl(url)
        except IOError as e:
            self.__logger.error(e)
        else:
            self.__logger.info("use seedfile:" + self.__seedfile)

    def __init__(self, seedfile):
        """the invoker should make sure the seedfile is exist"""
        # the file which have the seed sites
        self.__seedfile = seedfile
        # the unvisite sites
        self.__unvistedUrls = queue.Queue() # size is infinite
        # the visited sites
        self.__visitedUrls = []
        self.__logger = mslogger.MSLogger().getLogger()
        self.lock = threading.Lock()
        self._read_seed_file()
        self.config = msconfigparser.MSConfigParser(msconfigparser.default_cf)

    def popUrl(self):
        """
        get one unvisited url, not thread safe
        """
        url = None
#self.lock.acquire()
        try:
            url = self.__unvistedUrls.get(timeout=2) #2s
        except:
            url = None
#self.lock.release()
        return url

    def pushUrl(self, url):
        """
        add one unvisited url, not thread safe
        check url is valid or not??
        """
        if not self.checkVisitedUrl(url['url']):
            self.__logger.debug("new url:" + url['url'])
            self.lock.acquire()
            self.__unvistedUrls.put(url)
            self.lock.release()
            return True
        return False

    def pushVisitedUrl(self, url):
        """
        add the visited url to visitedUrls
        """
        if not self.checkVisitedUrl(url):
            self.lock.acquire()
            self.__visitedUrls.append(url)
            self.lock.release()
            return True
        return False

    def checkVisitedUrl(self, url):
        """
        check if the url in visitedUrls
        """
        self.lock.acquire()
        r = url in self.__visitedUrls
        self.lock.release()
        return r

if __name__ == "__main__":
    seedfile = "test/urls.txt"
    seedfile_path = os.getcwd() + os.sep + seedfile
    msurlstore = MSUrlStore(seedfile_path)

    url = msurlstore.popUrl()
    print(url['url'].strip())
    msurlstore.pushVisitedUrl(url)
    print(msurlstore.checkVisitedUrl(url['url']))
    url = msurlstore.popUrl()
    if url:
        print(url, msurlstore.checkVisitedUrl(url['url']))
    else:
        print("no url exit!")
    url = msurlstore.popUrl()
    if url:
        print("url:" , url['url'], msurlstore.checkVisitedUrl(url['url']))
    else:
        print("no url exit!")
    url1 = {'url':"http://www.baidu.com",'depth':1}
    print(msurlstore.pushUrl(url1))
    url2 = {'url':"http://www.baidu.com",'depth':2}
    print(msurlstore.pushUrl(url2))
    url = msurlstore.popUrl()
    print(url['url'].strip())
    url = msurlstore.popUrl()
    print("url:", url['url'].strip())

