import pandas as pd
from pytrends.request import TrendReq



def returnStats(keyword):


    print(keyword)

    res = TrendReq().suggestions(keyword=keyword)
    if len(res) == 1:
        searchTerm = (res[0])

    else:
        found = False
        for con in res:
            if con['type'] == 'United States Representative':
                searchTerm = (con)
                found = True
        
        if not found:
            searchTerm = res

    if type(searchTerm) == dict:
        return getPopularity(searchTerm)
    else:
        return {}



def getPopularity(congressman):
    
    pytrend = TrendReq()

    kw_list = [congressman['title']]
    pytrend.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')
    df = pytrend.interest_over_time()
    df = df.iloc[:, 0:1]

    popularity = dict()

    for row in df.iterrows():
        for x in (str(row[1]).split(' ')):
            if '\nName' in x:
                popularity[(str(row[0]).split(' ')[0])] = int(x.split('\nName:')[0])

    return popularity