#coding=utf-8

import re
import requests
from bs4 import BeautifulSoup

import mslogger
import msconfigparser

class MSURLHandler(object):
    """
    get the url and try to parse
    """
    def __init__(self, url, depth):
        self.__url = url
        self.__depth = depth
        self.__logger = mslogger.MSLogger().getLogger()
        self.__more_urls = []
        self.config = msconfigparser.MSConfigParser("")

    def isValidUrl(self, url):
        """
        what's valid url?
        target_url in spider.config
        """
        return url.startswith("http")

    def isValidUrlInAnchor(self, url):
        restr = self.config.getSpiderConfig("target_url")
        pattern = re.compile(restr)
        m = pattern.match(url)
        if m:
            return True
        else:
            return False

    def constructValidUrlFromAnchor(self, url):
        if url.startswith("http"):
            return url
        if url.startswith("javascript"):
            self.__logger.debug("js url:" + url)
            p = url.find("href=")
            urlInJS = url[p+5:].strip("'").strip('"')
            return constructValidUrlFromAnchor(urlInJS)
        last_slash = self.__url.rfind('/')
        if self.__url[last_slash-1] != '/' and self.__url[last_slash-2] != ':':
            return self.__url[0:last_slash] + '/' + url
        else:
            return self.__url + '/' + url

    def doHandle(self):
        """
        get the url content and parse, return the url in this page
        """
        if not self.isValidUrl(self.__url):
            self.__logger.warning("url:" + self.__url + " is not valid!")
            return self.__more_urls
        response = None
        try:
            #headers = {'user-agent': 'my-app/0.0.1'}
            crawl_timeout = self.config.getSpiderConfig('crawl_timeout')
            self.__logger.debug("crawl_timeout:" + crawl_timeout)
            response = requests.get(self.__url, timeout=int(crawl_timeout))
        except:
            self.__logger.warning("access " + self.__url + " fail!")
        else:
            if response:
                if ("text/html" == response.headers['content-type']):
                    self.handleResponse(response)
            else:
               self.__logger.warning("access " + self.__url + " fail!!")
        return self.__more_urls

    def handleResponse(self, response):
        if response.status_code == 200:
            response.encoding = "utf-8"
            content = response.text
            #TODO how to detect the encoding of the contents
            self.extractURLInAnchor(content)
            #TODO save the page
        else:
            self.__logger.warning("url:" + self.__url + " with response code" + str(response.status_code))

    def extractURLInAnchor(self, content):
        """
        extract the new url in <a>, and store in __more_urls
        """
        soup = BeautifulSoup(content, "html.parser")
        alinks =  soup.select("a")
        for link in alinks:
            newUrl = ""
            try:
                newUrl = link['href'].strip()
                #self.__logger.debug(newUrl)
            except KeyError as e:
                self.__logger.warning(link)
            else:
                if (self.isValidUrlInAnchor(newUrl)):
                    newUrl = self.constructValidUrlFromAnchor(newUrl)
#self.__logger.debug(newUrl)
                    self.__more_urls.append(newUrl)
        if len(self.__more_urls) <= 0:
            self.__logger.info(content)
    def saveContent(self, content):
        """
        try to save the content, no implementation now
        """
        pass

if __name__ == "__main__":
    url = "http://www.baidu.com"
    urlHandler = MSURLHandler(url, 1)
    newUrls = urlHandler.doHandle()
    for newUrl in newUrls:
        print(newUrl,";")

