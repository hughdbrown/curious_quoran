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
    
    #nltk.download('stopwords')
    stop = stopwords.words('english')
    extra_stopwords = ['mr', 'said', 'like', 'it', 'to', 'he', 'ms', 'dr', 're'] # Adding some custom stopwords 
    stop += extra_stopwords

    filtered =  [w.encode('ascii', 'ignore').lower().replace('\u2605','') for w in raw_wordlist if w.encode('ascii', 'ignore').lower().replace('\u2605','').replace('"','') not in stop]

    
    # Use wordnet lemmatizer on raw list
    lmtzr = WordNetLemmatizer()
    lem_words = [lmtzr.lemmatize(w).translate(None, punctuation) for w in filtered]
    return ' '.join(lem_words)

def preprocess_quora(quora):
	'''
	INPUT: Quora dump (raw string)
	OUTPUT: list of words to be fed into clean_up

	Turn raw list of individual questions into one raw string
	'''

	q_wlist = [q.split() for q in quora]
	qlist_tot = reduce(lambda x, y: x+y, q_wlist)
	return qlist_tot

def preprocess_gutenberg(gutenberg):
    '''
    INPUT: Gutenberg dump (list of string, each a book)
    OUTPUT: Pandas df with text for each book in each row

    '''
    books = [b.split() for b in gutenberg[0] if len(b) >0]
    book_dict = {ind:' '.join(b) for ind,b in enumerate(books)}
    #print book_dict
    book_df = pd.DataFrame.from_dict(book_dict, orient = 'index')
    #print books
    return book_df



if __name__ == "__main__":
    quora_user = open('quora_data.pkl')
    quora = pickle.load(quora_user)
    filtered = preprocess_quora(quora)
    print "Here's some clean Quora data: \n", clean_up(filtered)

    books = pickle.load(open('book_list.pkl'))
    bookdf = preprocess_gutenberg(books)
    print "Here's a clean dataframe of books: \n", bookdf[0].apply(lambda x: x.split()).apply(clean_up)


