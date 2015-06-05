from __future__ import print_function

import sys
import pickle
from string import punctuation

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

from coursera import get_coursera_data

reload(sys)
sys.setdefaultencoding("utf-8")

class TextParser():
    '''
    TextParser class with methods for NLP preprocessing from various sources
    '''
    def __init__(self):
        '''
        Only attribute is a master dataframe with all ref texts
        Dataframe columns will be title, description and type (podcast/course/ebook)
        '''
        self.df = None

    def clean_up(self, raw_wordlist):
        '''
        INPUT: list of raw text broken on whitespace
        OUTPUT: cleaned up string ready to be fed into a vectorizer
        
        Stem, lemmatize words in list and strip non alphabet chars and stopwords 
        '''
        
        # nltk.download('stopwords') => Only needed to do this once! Quite slow.
        stop = stopwords.words('english')
        extra_stopwords = ['mr', 'said', 'like', 'it', 'to', 'he', 'ms', 'dr', 're'] # Adding some custom stopwords 
        stop += extra_stopwords
        filtered =  [w.encode('ascii', 'ignore').lower().replace('\u2605','') for w in raw_wordlist if w.encode('ascii', 'ignore').lower().replace('\u2605','').replace('"','') not in stop]
        
        # Use wordnet lemmatizer on raw list
        lmtzr = WordNetLemmatizer()
        lem_words = [lmtzr.lemmatize(w).encode('utf-8').translate(None, punctuation) for w in filtered]
        return ' '.join(lem_words)

    def preprocess_quora(self, quora):
    	'''
    	INPUT: Quora dump (raw string)
    	OUTPUT: list of words to be fed into clean_up

    	Turn raw list of individual questions into one raw string
    	'''
    	q_wlist = [q.split() for q in quora]
    	qlist_tot = reduce(lambda x, y: x+y, q_wlist)
    	return qlist_tot

    def gutenberg_cat(self, path):
        '''
        INPUT: filepath to csv from Gutenberg SQL dump
        OUTPUT: dataframe with Title, Author, subject tags and pre-vectorized descriptions

        '''
        ebook = pd.read_csv(path)

        # Filter for only English books 
        english_only = ebook[ebook['flanguage']=='{en}']
        df = english_only[['ftitle', 'fsubjectname', 'ffriendlytitle']]

        # Rename columns
        df.columns = ['title', 'tags', 'title_auth']
        df = df.dropna()

        # Clean up cols
        for col in df.columns:
            df[col] = df[col].apply(lambda x: x.replace('{', '')).apply(lambda x: x.replace('}', '')).apply(lambda x: x.replace('"', ' '))
            df[col] = df[col].apply(lambda x: x.replace(',', ' '))

        df.subj_tags = df.tags.apply(lambda x: x.replace('--',''))

        # Make a composite book description column
        df['desc_tot'] = df['tags']+' '+ df['title']
        return df

    def assemble_df(self):
        '''
        INPUT: dataframe from gutenberg, podcasts
        OUTPUT: Aggregated dataframe with title, description, and resource type
        '''
        bookdf = self.gutenberg_cat('data/ebooks.csv')

        bookdf['cleaned_text'] = bookdf['desc_tot'].apply(lambda x: x.split()).apply(self.clean_up)
        bookdf = bookdf[['title_auth', 'cleaned_text']]

        with open("data/podcast_df.pkl") as f:
            pcast_df = pickle.load(f)
        pcast_df['desc'] = pcast_df['desc'].apply(lambda x: x.split()).apply(self.clean_up)
        bookdf.columns = pcast_df.columns
        course_df = get_coursera_data()
        course_df['desc'] = course_df['desc'].apply(lambda x: x.split()).apply(self.clean_up)

        # Set media types in new column:
        bookdf['type'] = 'ebook'
        pcast_df['type'] = 'podcast'
        self.df = pd.concat([pcast_df, bookdf, course_df], axis = 0)
        self.df = self.df.reset_index()
