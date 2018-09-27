#-*- coding: UTF-8 -*-

import mslogger
import msurlstore
import msurlhandler

class MSWork(object):
    """
    this work can be taken as a thread to handle the crawl jobs
    urlstore should support push/pop method about url(msurlstore.MSUrlStore)
    """
    def __init__(self, urlstore):
        self.__urlstore = urlstore
        self.__logger = mslogger.MSLogger()

    def doWork(self):
        url = self.__urlstore.popUrl()
        while url:
            urlHandler = msurlhandler.MSURLHandler(url)
            newUrls = urlHandler.doHandle()
            self.__urlstore.pushVisitedUrl(url)
            self.__logger.debug("visited:" + url)
            for newUrl in newUrls:
                self.__urlstore.pushUrl(newUrl)
            url = self.__urlstore.popUrl()

if __name__ == "__main__":
    import msurlstore
    import os
    seedfile = "test/urls_test.txt"
    seedfile_path = os.getcwd() + os.sep + seedfile
    urlstore = msurlstore.MSUrlStore(seedfile_path)

    msWork = MSWork(urlstore)
    msWork.doWork()

    url = urlstore.popUrl()
    while url:
        print(url, ";")
        url = urlstore.popUrl()
