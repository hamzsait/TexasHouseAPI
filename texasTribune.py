import os
from os import environ
import pprint
import json
from twitterStats import twitterCongress
from facebookStats import facebookCongress
from time import sleep
from pymongo import MongoClient
from webdriver import getWebdriver

# from password import password

# testing adding

def connectMongo(local = False):

    # if not local:
    #     password = environ['DB_PASSWORD']

    cluster = MongoClient(f'mongodb+srv://hello:hello@cluster0.txmw4.mongodb.net/houseoftexas?retryWrites=true&w=majority')
    db = cluster['houseoftexas']
    collection = db['texas_congress']
    return collection

def scrapeTexasCongress(local = False):

    driver = getWebdriver(local = local)

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

            data = dict()

            data['_id'] = int(driver.find_element_by_xpath("//*[contains(text(),'District')]").text.split(' ')[1])

            try:
                email = json.loads(driver.find_element_by_xpath("//*[contains(text(),'https://schema.org/')]").get_attribute('innerHTML'))['mainEntity'][0]['contactPoint'][0]['email']
                data['email'] = email
            except:
                data['email'] = 'No Email'

            try:
                phone = json.loads(driver.find_element_by_xpath("//*[contains(text(),'https://schema.org/')]").get_attribute('innerHTML'))['mainEntity'][0]['contactPoint'][0]['telephone']
                data['phone'] = phone
            except:
                data['phone'] = 'No Phone'

            try:
                image = json.loads(driver.find_element_by_xpath("//*[contains(text(),'https://schema.org/')]").get_attribute('innerHTML'))['image'][0]['url']
                data['image'] = image
            except:
                data['image'] = 'No Image'

            try:
                party = json.loads(driver.find_element_by_xpath("//*[contains(text(),'https://schema.org/')]").get_attribute('innerHTML'))['keywords'][3]
                data['party'] = party
            except:
                data['party'] = 'No Party'

            buttons = driver.find_elements_by_class_name("c-button")
            for button in buttons:
                button_link = button.get_attribute("href")

                if ('facebook' in button_link):
                    data['facebook'] = facebookCongress(button_link, local = local)

                if('twitter' in button_link):

                    data['twitter'] = twitterCongress(button_link, local = local)
            

            tx_congress[(driver.find_element_by_class_name('politician-header').text.split('\n')[0].split('U.S. Representative ')[1].replace('.',''))] = data
    driver.close()
    return tx_congress

def printDB(db):

    for x in db.find({}):
        pprint.pprint(x)

def deleteDB(db):
    db.delete_many({})

def initDB(db, tx_congress):
    for congressman in tx_congress:
        db.insert_one({'_id':tx_congress[congressman]['_id'],'name':congressman,'email':tx_congress[congressman]['email'], 'image':tx_congress[congressman]['image'],'phone':tx_congress[congressman]['phone'],'twitter':tx_congress[congressman]['twitter'], 'facebook':tx_congress[congressman]['facebook']})

def updateDB(db, tx_congress):
    for congressman in tx_congress:
        filter = {'_id':tx_congress[congressman]['_id']}
        updated_values = {'$set':{'name':congressman,'party':tx_congress[congressman]['party'],'email':tx_congress[congressman]['email'], 'image':tx_congress[congressman]['image'],'phone':tx_congress[congressman]['phone'],'twitter':tx_congress[congressman]['twitter'], 'facebook':tx_congress[congressman]['facebook']}}
        db.update_one(filter, updated_values)

def main():

    local = True

    #db = connectMongo(local)
    # deleteDB(db)
    tx_congress = scrapeTexasCongress(local)
    # initDB(db, tx_congress)
    # updateDB(db,tx_congress)
    #printDB(db)


main()
