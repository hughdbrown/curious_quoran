import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
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
        self.quora = pickle.load(open("data/clean_quora.pkl"))
        self.quora = pd.Series(self.quora)
        print "The quora data as it is read in", self.quora
        self.distances = []
        print self.df

    def vectorize(self):
        '''
        INPUT: list of cleaned, lemmatized and filtered text
        OUTPUT: cleaned up string ready to be fed into a vectorizer
        
        Stem, lemmatize words in list and strip non alphabet chars and stopwords 
        '''
        vec = TfidfVectorizer()
        doc_vecs_sparse = vec.fit_transform(self.df.desc.values)
        doc_vecs = doc_vecs_sparse.toarray()
        quora_vec = vec.transform(self.quora.values)

        print "Shape of doc vector array", doc_vecs.shape
        print "Shape of quora vector", quora_vec.shape
        
        for doc in doc_vecs:
            doc = doc.reshape(1,doc.shape[0])
            print doc.shape
            print quora_vec.shape
            self.distances.append(cosine(quora_vec, doc))

        #self.distances = [cosine(quora_vec, d) for d in doc_vecs]


    def recommend(self):
        '''
        INPUT: np array of distances
        OUTPUT: names and types of recommendations
        '''

        top_ten = np.argsort(self.distances)[:10]
        return top_ten


if __name__ == "__main__":

    rec = Recommender()
    test = rec.vectorize()
    # recs = read.df.ix[top_ten_ind]
    # return recs[['title', 'type']]

