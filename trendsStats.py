import pandas as pd
from pytrends.request import TrendReq



def getSuggestion(keyword):


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
        return searchList(searchTerm)
    else:
        return f'None for {searchTerm}'



def searchList(congressman):
    
    pytrend = TrendReq()

    kw_list = [congressman['title']]
    pytrend.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')
    df = pytrend.interest_over_time()

    return df.iloc[:, 0:1]
