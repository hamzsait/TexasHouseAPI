import os
from selenium import webdriver
from time import sleep
from pymongo import MongoClient
from password import password
import pprint


def getWebdriver(local = False):

    if local:
        return webdriver.Chrome()

    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dec-sh-usage")

    driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)

    return driver

def connectMongo(password = password()):

    cluster = MongoClient(f'mongodb+srv://webuser:{password}@cluster0.gg0wl.mongodb.net/texas_congress_db?retryWrites=true&w=majority')
    db = cluster['Cluster0']
    collection = db['texas_congress']
    return collection

def scrapeTexasCongress():
    driver = getWebdriver(local = True)

    driver.get("https://www.texastribune.org/directory/#congress")
    sleep(2)
    table = driver.find_element_by_class_name("c-table")
    elems = table.find_elements_by_xpath("//a[@href]")

    tx_house_links = []
    within_house_links = False
    knock_next = False
    for elem in elems:

        link = elem.get_attribute("href")

        if "us-house/1/" in link:
            within_house_links = True

        if within_house_links:
            tx_house_links.append(link)

        if knock_next == True:
            tx_house_links.append(link)
            break

        if "us-house/36/" in link:
            knock_next = True
            within_house_links = False

    tx_congress = dict()
    for link in tx_house_links:


        if 'us-house' not in link:
            driver.get(link)
            sleep(0.5)

            social_media = dict()

            buttons = driver.find_elements_by_class_name("c-button")
            for button in buttons:
                button_link = button.get_attribute("href")

                if ('facebook' in button_link):
                    social_media['facebook'] = button_link

                if('twitter' in button_link):
                    social_media['twitter'] = button_link

            tx_congress[(driver.find_element_by_class_name('politician-header').text.split('\n')[0].split('U.S. Representative ')[1].replace('.',''))] = social_media
    driver.close()
    return tx_congress

def printDB(db):

    for x in db.find({}):
        pprint.pprint(x)

def deleteDB(db):
    db.delete_many({})

def initDB(db, tx_congress):
    for congressman in tx_congress:
        db.insert_one({'name':congressman})

def updateDB(db, tx_congress):
    for congressman in tx_congress:
        filter = {'name': congressman}
        updated_values = {'$set':{'twitter':tx_congress[congressman]['twitter'], 'facebook':tx_congress[congressman]['facebook']}}
        db.update_one(filter, updated_values)

def main():
    db = connectMongo()
    tx_congress = scrapeTexasCongress()
    updateDB(db,tx_congress)
    printDB(db)

main()
