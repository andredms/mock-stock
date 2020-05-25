##############################
# Purpose: Scrape the ASX    #
# Author:  Andre de Moeller  #
# Created: 18/05/2020        #
# Modified: 19/05/2020       #
##############################
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import sys

def getLink(acronym):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    #append company acronym to url
    url = "https://www.asx.com.au/asx/share-price-research/company/" + acronym
    driver.get(url)

    #give enough time for javascript to load
    sleep(0.5)

    #get raw html
    html = driver.page_source

    driver.quit()
    #process html
    new_html = BeautifulSoup(html, "html.parser")
    #get element containing the increase/decrease %
    spans = new_html.find_all("span", {"class" : "overview-change-percentage"})
    for span in spans:
        ele = span.text.replace('%', '')
        return ele