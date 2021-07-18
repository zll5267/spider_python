# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests, sys
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import json

def get_basic_info():
    basic_info = {}
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')
    browser = webdriver.Chrome(options = options)
    browser.get('http://www.12365auto.com/review/kb.shtml')
    # js1="document.documentElement.scrollTop=10000"
    # browser.execute_script(js1)
    # js2="document.documentElement.scrollTop=0"
    # browser.execute_script(js2)
    # time.sleep(2)
    #print(browser.page_source)
    brands_button = browser.find_element_by_id('brands')
    brands_button.click()
    bsoup = BeautifulSoup(browser.page_source, features="html.parser")
    brand_options = bsoup.select('#brands option')
    brands = [] # element is (name, value)
    basic_info["brands"] = []
    for brand_option in brand_options:
        #print(brand_option)
        #brands option format:<option value="109">Z-中华</option>
        brand_name = brand_option.string
        brand_value = brand_option.attrs["value"]
        if len(brand_value) > 0:
            #print(brand_name, brand_value)
            brands.append((brand_name, brand_value))


    #browser.find_element_by_xpath('//div[@class="button"]').click()
    #time.sleep(1)
    #browser.find_element_by_css_selector("select#nr>option:nth-child(2)").click()
    #print(Select(sel).first_selected_option("select#brands"))
    test_brand = "650"
    for brand_element in brands:
        brand = {}
        if test_brand != "-1" and brand_element[1] != test_brand:
            continue
        brand["name"] = brand_element[0]
        brand["value"] = brand_element[1]
        sel = browser.find_element_by_css_selector("select#brands")
        print("select brand:{}, value:{}".format(brand_element[0], brand_element[1]))
        Select(sel).select_by_value(brand_element[1])
        #browser.refresh()
        brand_bsoup = BeautifulSoup(browser.page_source, features="html.parser")
        #print(bsoup.select('#series option'))
        series_options = brand_bsoup.select('#series option')
        series = [] # element is (name, value, bid)
        brand["series"] = []
        for seria_option in series_options:
            #print(seria_option)
            #series option format: <option bid="266" value="903">假日风情</option>
            seria_name = seria_option.string
            seria_value = seria_option.attrs["value"]
            if len(seria_value) > 0:
                seria_bid = seria_option.attrs["bid"]
                #print(seria_name, seria_value, seria_bid)
                series.append((seria_name, seria_value, seria_bid))

        test_seria = "-1"
        for seria_element in series:
            if test_seria != "-1":
                if test_seria == -2:
                    break
                else:
                    test_seria = -2
            serial = {}
            serial["name"] = seria_element[0]
            serial["value"] = seria_element[1]
            serial["bid"] = seria_element[2]
            print("select serial:{}, value:{}".format(seria_element[0], seria_element[1]))
            #why there is twice select?? need to figure out the reason
            series_sel = browser.find_element_by_css_selector("select#series")
            #Select(series_sel).select_by_value(seria_element[1])
            Select(series_sel).select_by_value(seria_element[1])
            serial_bsoup = BeautifulSoup(browser.page_source, features="html.parser")
            #print(serial_bsoup.select('#models option'))
            series_sel = browser.find_element_by_css_selector("select#series")
            #Select(series_sel).select_by_value(seria_element[1])
            Select(series_sel).select_by_value(seria_element[1])

            #browser.refresh()
            serial_bsoup = BeautifulSoup(browser.page_source, features="html.parser")
            #print(serial_bsoup.select('#series option'))
            #print(serial_bsoup.select('#models option'))
            models_options = serial_bsoup.select('#models option')
            models = [] # element is (name, value, data-fuel)
            serial["models"] = []
            for model_option in models_options:
                #print(model_option)
                #series option format: <option data-fuel="1" value="49853">2015款 ACS35 35i</option>
                model_name = model_option.string
                model_value = model_option.attrs["value"]
                if len(model_value) > 0:
                    model_datafuel = model_option.attrs["data-fuel"]
                    #print(model_name, model_value, model_datafuel)
                    models.append((model_name, model_value, model_datafuel))
            for model_element in models:
                model = {}
                model["name"] = model_element[0]
                model["value"] = model_element[1]
                model["datafuel"] = model_element[2]
                print("model name:{}, value:{}".format(model_element[0], model_element[1]))
                print("brand name:{}, brand_value:{};serial_name:{}, serial_value:{};model_name:{},model_value{}"
                .format(brand_element[0], brand_element[1], seria_element[0], seria_element[1], model_element[0], model_element[1]))
                serial["models"].append(model)
            brand["series"].append(serial)
        basic_info["brands"].append(brand)
    return basic_info

if __name__ == "__main__":
    basic_info = get_basic_info()
    with open("basic_info.json", "w", encoding ='utf8') as output_file:
        json.dump(basic_info, output_file, indent=4, ensure_ascii = False)
