import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import pickle

def get_coursera_data():
    '''
    INPUT: dict from FeedWrangler API
    OUTPUT: dict with title, description for top 50 most popular podcasts

    Accesses the Coursera course catalog
    '''

    courses = requests.get('https://api.coursera.org/api/catalog.v1/courses')
    master_dict = courses.json()
    course_dict = master_dict["elements"]

    podcast_df = pd.DataFrame.from_dict(course_dict)
    return podcast_df

if __name__=="__main__":
    print get_coursera_data()