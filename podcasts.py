from __future__ import print_function

import pickle

import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_podcast_data():
    '''
    INPUT: dict from FeedWrangler API
    OUTPUT: DF with title, description for top 50 most popular podcasts

    Accesses a list of the top 50 podcasts via FeedWrangler API, loops over ids and obtains descriptions with another API call
    '''

    top_fifty = requests.get('https://feedwrangler.net/api/v2/podcasts/popular')
    master_dict = top_fifty.json()
    podcast_dict = master_dict["podcasts"]
    podcast_df = pd.DataFrame.from_dict(podcast_dict)
    return podcast_df


def pcast_desc(rss_url):
    '''
    INPUT: URL of RSS episode feed for each podcast 
    OUTPUT: aggregate text from all recent episode descriptions

    Collects and cleans episode descriptions from podcast episodes using BeautifulSoup
    '''
    description = requests.get(rss_url).text
    soup = BeautifulSoup(description, 'xml')
    summary_text = str(soup.findAll('summary')) # Pick out episode summaries only
    text = soup.get_text()
    clean = summary_text.replace('\n', '').replace('<itunes:summary>','').replace('</itunes:summary>','')
    return clean


if __name__=="__main__":
    df = get_podcast_data()
    df['desc'] = df['feed_url'].apply(lambda x: pcast_desc(x)) # Collect descriptions using feed urls
    df = df[['title', 'desc']]
    df.desc = df['desc'].apply(lambda x: x.replace('[','')).apply(lambda x: x.replace('[',''))
    pickle.dump(df, open("data/podcast_df.pkl", "wb")) # Dump raw data to be processed by parser class