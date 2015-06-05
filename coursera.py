from __future__ import print_function

import pandas as pd
import requests

def get_coursera_data():
    '''
    INPUT: dict from FeedWrangler API
    OUTPUT: dict with title, description for top 50 most popular podcasts

    Accesses the Coursera course catalog and assembles dataframe with course title and description
    '''

    courses = requests.get('https://api.coursera.org/api/catalog.v1/courses')
    master_dict = courses.json()
    course_dict = master_dict["elements"]

    df = pd.DataFrame.from_dict(course_dict)
    df['type']= "course"
    df = df[['name', 'shortName', 'type']]
    df['shortName'] = df['name']+' '+df['shortName'] # Aggregate name and tags for description
    df.columns = ['title', 'desc', 'type']
    print("There are {0} courses in the catalog.".format(len(df)))
    return df

if __name__=="__main__":
    df= get_coursera_data()
    print(df)