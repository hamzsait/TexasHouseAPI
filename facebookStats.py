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

def facebookCongress(username, local = False):

    driver = getWebdriver(local = local)
