import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Recommender():
    '''
    
    Recommender class with methods that generate most (cosine) similar resources for a given block of Quora text
    
    '''

    def __init__(self):
        '''
        Only attribute is a master dataframe with all ref texts
        Cols of the dataframe: verbose description, clean description
        '''
        self.df = pickle.load(open("data/master_df.pkl"))
        self.quora = pd.Series(pickle.load(open("data/clean_quora.pkl")))
        self.distances = []
        
    def vectorize(self):
        '''
        INPUT: list of cleaned, lemmatized and filtered text
        OUTPUT: cleaned up string ready to be fed into a vectorizer
        
        Vectorizes documents in the corpus (resources from PG, Coursera, etc.) and computes cosine similarity
        with a user's Quora profile information or Question Page 
        '''

        vec = TfidfVectorizer(ngram_range = (1,5), max_features = 5000)
        #vec = TfidfVectorizer(ngram_range = (2,3), max_features=5000)
        doc_vecs_sparse = vec.fit_transform(self.df.desc.values)
        quora_vec = vec.transform(self.quora.values)
        self.distances = cosine_similarity(quora_vec, doc_vecs_sparse)[0]
        

    def recommend(self):
        '''
        INPUT: np array of distances
        OUTPUT: names and types of recommendations
        '''

        top_ten = np.argsort(self.distances)[::-1]
        return top_ten[:20]