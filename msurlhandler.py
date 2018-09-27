#coding=utf-8

import requests
from bs4 import BeautifulSoup

import mslogger

class MSURLHandler(object):
    """
    get the url and try to parse
    """
    def __init__(self, url):
        self.__url = url
        self.__logger = mslogger.MSLogger()
        self.__more_urls = []

    def isValidUrl(self, url):
        """
        what's valid url?
        """
        return url.startswith("http")

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
            response = requests.get(self.__url, timeout=10) #TODO get from config file
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
                #self.__logger.debug(newurl)
                if (self.isValidUrl(newUrl)):
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
    urlHandler = MSURLHandler(url)
    newUrls = urlHandler.doHandle()
    for newUrl in newUrls:
        print(newUrl,";")