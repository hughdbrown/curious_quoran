import pandas as pd
import requests

def get_podcast_data():
    '''
    INPUT: dict from FeedWrangler API
    OUTPUT: dict with title, description for top 50 most popular podcasts

    Accesses a list of the top 50 podcasts via FeedWrangler API
    '''

    top_fifty = requests.get('https://feedwrangler.net/api/v2/podcasts/popular')
    master_dict = top_fifty.json()
    podcast_dict = master_dict["podcasts"]
    for pcast in podcast_dict:
        print pcast['title']



if __name__=="__main__":
    get_podcast_data()
