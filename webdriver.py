from selenium import webdriver
import os
from os import environ

def getWebdriver(local = False):

    if local:
        return webdriver.Chrome()

    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dec-sh-usage")

    return webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), options=op)

    