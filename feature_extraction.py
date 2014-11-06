from nltk.stem.wordnet import WordNetLemmatizer
from string import punctuation
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize

def clean_up(raw_wordlist):
    '''
    INPUT: list of raw text broken on whitespace
    OUTPUT: cleaned up string ready to be fed into a vectorizer
    
    Stem, lemmatize words in list and strip non alphabet chars and stopwords 
    '''
    
    nltk.download('stopwords')
    stop = stopwords.words('english')
    extra_stopwords = ['mr', 'said', 'like', 'it', 'to', 'he', 'ms', 'dr', 're'] # Adding some custom stopwords 
    stop += extra_stopwords

    filtered =  [w.encode('ascii', 'ignore').lower().replace('\u2605','') for w in raw_wordlist if w.encode('ascii', 'ignore').lower().replace('\u2605','').replace('"','') not in stop]

    
    # Use wordnet lemmatizer on raw list
    lmtzr = WordNetLemmatizer()
    lem_words = [lmtzr.lemmatize(w).translate(None, punctuation) for w in filtered]
    return ' '.join(lem_words)

def preprocess_quora(quora_dump):
	'''
	INPUT: Quora dump in pickle form (raw string)
	OUTPUT: list of words to be fed into clean_up

	Turn raw list of individual questions into one raw string
	'''

	q_wlist = [q.split() for q in quora]
	qlist_tot = reduce(lambda x, y: x+y, q_wlist)
	return qlist_tot

if __name__ == "__main__":
    quora_user = open('quora_data.pkl')
    quora = pickle.load(quora_user)
    filtered = preprocess_quora(quora)
    print clean_up(filtered)


