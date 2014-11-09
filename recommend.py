import pickle
import pandas as pd
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
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
        self.df = pickle.load(open("master_df.pkl"))
        self.quora = pickle.load(open("clean_quora.pkl"))
        self.distances = None

    def vectorize(self, list):
        '''
        INPUT: list of cleaned, lemmatized and filtered text
        OUTPUT: cleaned up string ready to be fed into a vectorizer
        
        Stem, lemmatize words in list and strip non alphabet chars and stopwords 
        '''
        vec = TfidfVectorizer()
        doc_vecs = [vec.fit_transform(doc) for doc in df]
        quora_vec = vec.transform(self.quora)

        # Get pairwise distances using pdist, rank and argsort
        self.distances = "something"


    def recommend(self):
        '''
        INPUT: np array of distances
        OUTPUT: names and types of recommendations
        '''

        top_ten = np.argsort(self.distances)[:10]
        return top_ten





if __name__ == "__main__":

    rec = Recommender()
    top_ten_ind = rec.recommend()
    recs = read.df.ix[top_ten_ind]
    return recs[['title', 'type']]

