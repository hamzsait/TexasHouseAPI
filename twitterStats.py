import os
from os import environ
from selenium import webdriver
from time import sleep

def getWebdriver(local = False):

    if local:
        return webdriver.Chrome()

    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dec-sh-usage")

    driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), options=op)

    return driver

def twitterCongress(link, local = False):

    driver = getWebdriver(local = local)

    twitter_data = dict()
    twitter_data['url'] = link
    twitter_data['handle'] = (link.split('/')[-1])
     
    driver.get(f'https://twitter.com/{twitter_data["handle"]}')
    sleep(2)
    followers = driver.find_element_by_xpath("//*[contains(text(),'Followers')]")
    twitter_data['followers'] = (followers.find_element_by_xpath("./../..").text.split(' ')[0])
    driver.close()


    return twitter_data