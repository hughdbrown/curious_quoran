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
    
    Stem, lemmatize words in list and strip non alphabet chars. 
    '''
    
    nltk.download('stopwords')
    stop = stopwords.words('english')
    extra_stopwords = ['mr', 'said', 'like', 'it', 'to', 'he', 'ms', 'dr', 're']
    stop += extra_stopwords
    
    # Use wordnet lemmatizer on raw list
    lmtzr = WordNetLemmatizer()
    lem_words = [lmtzr.lemmatize(w).translate(None, punctuation) for w in raw_wordlist]
    return ' '.join(lem_words)