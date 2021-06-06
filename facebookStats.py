from webdriver import getWebdriver
from time import sleep

def makeConnection(driver, link):
    try:
        sleep(30)
        driver.get(link)
        followers = driver.find_element_by_xpath("//*[contains(text(),'like this')]")
        facebook_data['followers'] = (followers.find_element_by_xpath("./..").text)
    except:
        makeConnection(driver,link)

def facebookCongress(link, local = False):

    driver = getWebdriver(local = local)

    facebook_data = dict()

    facebook_data['handle'] = (link.split('/')[-1])
    print(facebook_data['handle'])
    print(link)
    driver.get(f'https://facebook.com/{facebook_data["handle"]}')
    sleep(2)

    try:
        followers = driver.find_element_by_xpath("//*[contains(text(),'like this')]")
        facebook_data['followers'] = (followers.find_element_by_xpath("./..").text.split(' '))
    except:
        makeConnection(driver,f'https://facebook.com/{facebook_data["handle"]}')


    print(facebook_data['followers'])

    driver.close()

    return link

