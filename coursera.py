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

    df = pd.DataFrame.from_dict(course_dict)
    df['type']= "course"
    df = df[['name', 'shortName', 'type']]
    df['desc'] = df['name']+' '+df['shortName']
    df.columns = ['title', 'desc1', 'type', 'desc']
    del df['desc1']
    df = df[['title', 'desc', 'type']]
    print "There are {0} courses in the catalog.".format(len(df))
    return df

if __name__=="__main__":
    df= get_coursera_data()
    print df