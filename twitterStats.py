from webdriver import getWebdriver
from time import sleep

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