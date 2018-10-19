#-*- coding: UTF-8 -*-
import threading

import mslogger
import msurlstore
import msurlhandler
import msconfigparser

class MSWork(threading.Thread):
    """
    this work can be taken as a thread to handle the crawl jobs
    urlstore should support push/pop method about url(msurlstore.MSUrlStore)
    """
    def __init__(self, urlstore):
        threading.Thread.__init__(self)
        self.__urlstore = urlstore
        self.__logger = mslogger.MSLogger().getLogger()
        self.config = msconfigparser.MSConfigParser(msconfigparser.default_cf)

    def doWork(self):
        url = self.__urlstore.popUrl()
        while url:
            url_depth = url['depth']
            urlHandler = msurlhandler.MSURLHandler(url['url'], url_depth)
            newUrls = urlHandler.doHandle()
            self.__urlstore.pushVisitedUrl(url['url'])
            self.__logger.debug("visited:" + url['url'])
            self.__logger.debug('depth:' + str(url_depth))
            max_depth = int(self.config.getSpiderConfig("max_depth"))
            if url_depth < max_depth:
                for newUrl in newUrls:
                    self.__urlstore.pushUrl({'url':newUrl,'depth':url_depth+1})
            else:
                self.__logger.warning("max_depth reached")
            url = self.__urlstore.popUrl()

    def run(self):
        start_str = "thread %s stared!" % threading.current_thread().name
        self.__logger.debug(start_str)
        self.doWork()
        stop_str = "thread %s stopped!" % threading.current_thread().name
        self.__logger.debug(stop_str)

if __name__ == "__main__":
    import msurlstore
    import os
    seedfile = "test/urls_test.txt"
    seedfile_path = os.getcwd() + os.sep + seedfile
    urlstore = msurlstore.MSUrlStore(seedfile_path)

    msWork = MSWork(urlstore)
    msWork.doWork() #msWork.start()

    try:
        url = urlstore.popUrl()
        while url:
            print(url)
            url = urlstore.popUrl()
    except KeyboardInterrupt:
        pass

