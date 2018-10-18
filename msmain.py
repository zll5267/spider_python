#coding=utf-8

import os
import sys

import msargparser
import msconfigparser
import msurlstore
import mswork

if __name__ == "__main__":
    msarg = msargparser.MSArgParser(sys.argv[1:])
    print("config file:" + msarg.getConfigFile())

    msconfig = msconfigparser.MSConfigParser(msarg.getConfigFile())

    seedfile_path = os.getcwd() + os.sep + msconfig.urlListFile
    print("seed file:" + seedfile_path)
    urlstore = msurlstore.MSUrlStore(seedfile_path)

    threads = []
    for i in range(msconfig.threadCount):
        msWork = mswork.MSWork(urlstore)
        #msWork.doWork()
        msWork.start()
        threads.append(msWork)

    for thread in threads:
        thread.join()

