import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_podcast_data():
    '''
    INPUT: dict from FeedWrangler API
    OUTPUT: dict with title, description for top 50 most popular podcasts

    Accesses a list of the top 50 podcasts via FeedWrangler API, loops over ids and obtains descriptions with another API call
    '''

    top_fifty = requests.get('https://feedwrangler.net/api/v2/podcasts/popular')
    master_dict = top_fifty.json()
    podcast_dict = master_dict["podcasts"]

    podcast_desc_list = []
    for pcast in podcast_dict:
        print pcast['title']
        print pcast['feed_url']

        # Get descriptions by calling the appropriate page
        url = pcast['feed_url']
        description = requests.get(url).text
        print description

        # soup = BeautifulSoup(description)
        # podcast_desc_list.append(soup.get_text())
    return podcast_desc_list


if __name__=="__main__":
    get_podcast_data()
