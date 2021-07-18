# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests, sys
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import json
import re

def extract_comment_rank(bfs):
    rank_catgory_result = "unknow"
    rank_level_result = "-1"
    rank_categorys = bfs.select('.df_ph span')
    rank_levels = bfs.select('.df_ph em')
    #should only one here
    for rank_category in rank_categorys:
        #print(rank_category.string)
        if rank_category.string:
            rank_catgory_result = rank_category.string
    #should only one here
    for rank_level in rank_levels:
        #print(rank_level.string)
        if rank_level.string:
            rank_level_result = rank_level.string
    return rank_catgory_result + rank_level_result
def extract_comment_score(bfs):
    result = 0
    comment_scores = bfs.select('.df_sh b')
    #should only one here
    for comment_score in comment_scores:
        #print(comment_score.string)
        result = float(comment_score.string)
    return result
def extract_comment_number(bfs):
    result = 0
    comment_elements = bfs.select('.df_sh strong')
    #should only one here
    for comment_element in comment_elements:
        #print(comment_element.string)
        comment_number = re.findall(r"基于(.+?)个点评",comment_element.string)
        result = int(comment_number[0])
    return result

"""
    return (comment_number, comment_score, rank_level)
    e.g.:
"""
def extract_url_info(target_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')
    browser = webdriver.Chrome(options = options)
    browser.get(target_url)
    bsoup = BeautifulSoup(browser.page_source, features="html.parser")
    comment_number = extract_comment_number(bsoup)
    comment_score = extract_comment_score(bsoup)
    comment_rank = extract_comment_rank(bsoup)
    #print(comment_number, comment_score, comment_rank)
    return (comment_number, comment_score, comment_rank)

def spider_by_file():
    #file_name = "test.json"
    file_name = "basic_info.json"
    target_url_template = "http://www.12365auto.com/review/{}_{}_0_1.shtml"
    #target_url_template = "http://www.12365auto.com/review/2263_44786_0_1.shtml"
    basic_info = {}
    with open(file_name, "r") as infile:
       basic_info = json.load(infile)
    if basic_info:
        for brand in basic_info["brands"]:
            for serial in brand["series"]:
                for model in serial["models"]:
                    #print(model)
                    target_url = target_url_template.format(serial["value"], model["value"])
                    print(target_url)
                    extract_result = extract_url_info(target_url)
                    print("{}:{}:{}=>点评人数:{},平均分{}, {}"
                          .format(brand["name"], serial["name"], model["name"],
                                  extract_result[0], extract_result[1], extract_result[2]))

if __name__ == "__main__":
    spider_by_file()
