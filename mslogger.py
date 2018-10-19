#-*- coding: UTF-8 -*-
import logging
import os
import time
import msutils

@msutils.singleton
class MSLogger(object):
    """
    logger implementation
    not good, need improve!!
    """

    def __setfilelogger(self, logger):
        #logger.setLevel(logging.INFO)
        filename = time.strftime('%Y%m%d%H', time.localtime(time.time()))
        log_path = os.getcwd() + self.__log_folder
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_name = log_path + filename + '.log'
        logfile = log_name
        fh = logging.FileHandler(logfile)
        fh.setLevel(self.__log_level)
        formatter = logging.Formatter(self.__log_fmt)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    def __setconsolelog(self, logger):
        ch = logging.StreamHandler()
        ch.setLevel(self.__log_level)
        formatter = logging.Formatter(self.__log_fmt)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    def __init__(self, logLevel=None, logFolder=None, logFmt=None):
        """@param logLevel, see more info in logging
           @param logFolder, the relative folder according the cwd
           @param logFmt, see more info in logging
        """

        if logLevel:
            self.__log_level = logLevel
        else:
            self.__log_level = logging.DEBUG

        if logFolder:
            self.__log_folder = logFolder
        else:
            self.__log_folder = '/test/logs/'

        if logFmt:
            self.__log_fmt = logFmt
        else:
            self.__log_fmt = '%(asctime)s-[%(thread)d]-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'

        self.__logger = logging.getLogger()

        self.__logger.setLevel(self.__log_level)
        self.__setfilelogger(self.__logger)
        self.__setconsolelog(self.__logger)

    def getLogger(self):
        return self.__logger;

    def debug(self, msg):
        self.__logger.debug(msg)

    def info(self, msg):
        self.__logger.info(msg)

    def warning(self, msg):
        self.__logger.warning(msg)

    def error(self, msg):
        self.__logger.error(msg)

if __name__ == "__main__":
    myLogger = MSLogger()
    myLogger2 = MSLogger()
    if myLogger != myLogger2:
        print("error .....")
    myLogger.debug("debug msg")
    myLogger.info("info msg")
    myLogger.warning("warning msg")
    myLogger.error("error msg")

    myLogger.getLogger().debug("debug msg")
    myLogger.getLogger().info("info msg")
    myLogger.getLogger().warning("warning msg")
    myLogger.getLogger().error("error msg")
