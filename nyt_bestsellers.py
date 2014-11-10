import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import pickle

def get_nyt_data():
    '''
    INPUT: dict from NYTimes API with bestseller data
    OUTPUT: dataframe with book data (title author pubdate) and brief review

    Accesses a list of NYTimes bestsellers, 
    '''

    bestsellers = requests.get('http://api.nytimes.com/svc/books/v3/reviews')
    master_dict = bestsellers
    bs_dict = master_dict["results"]

    print bs_dict

    bs_df = pd.DataFrame.from_dict(bs_dict)
    print bs_df
    return bs_df

if __name__=="__main__":
    get_nyt_data()