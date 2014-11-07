import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

def get_podcast_data():
    '''
    INPUT: dict from FeedWrangler API
    OUTPUT: dict with title, description for top 50 most popular podcasts

    Accesses a list of the top 50 podcasts via FeedWrangler API, loops over ids and obtains descriptions with another API call
    '''

    top_fifty = requests.get('https://feedwrangler.net/api/v2/podcasts/popular')
    master_dict = top_fifty.json()
    podcast_dict = master_dict["podcasts"]

    podcast_df = pd.DataFrame.from_dict(podcast_dict)
    return podcast_df


def pcast_desc(rss_url):

    description = requests.get(rss_url).text
   
    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(description, 'xml')

    summary_text = str(soup.findAll('summary'))
    # print summary_text

    text = soup.get_text()
    clean = summary_text.replace('\n', '').replace('<itunes:summary>','').replace('</itunes:summary>','')
    #print clean
    return clean



if __name__=="__main__":
    df = get_podcast_data()
    df['desc'] = df['feed_url'].apply(lambda x: pcast_desc(x))
    pickle.dump(df,open("podcasts.pkl"))