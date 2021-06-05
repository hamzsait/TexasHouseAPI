from webdriver import getWebdriver
from time import sleep


def facebookCongress(link, local = False):

    driver = getWebdriver(local = local)

    facebook_data = dict()

    facebook_data['handle'] = (link.split('/')[-1])
    print(facebook_data['handle'])
    print(link)
    driver.get(f'https://facebook.com/{facebook_data["handle"]}')
    sleep(2)

    driver.close()

    return link

