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

class TextParser():
    '''
    TextParser class with methods for NLP preprocessing from various sources

    '''

    def __init__(self):
        '''
        Only attribute is a master dataframe with all ref texts
        Cols of the dataframe: verbose description, clean description
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
        lem_words = [lmtzr.lemmatize(w).translate(None, punctuation) for w in filtered]
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

    def preprocess_gutenberg(self, gutenberg):
        '''
        INPUT: Gutenberg dump (list of string, each a book)
        OUTPUT: Pandas df with text for each book in each row

        '''

        books = [b.split() for b in gutenberg if len(b) >0]
        print "Here's a book:", books[0]
        book_dict = {ind:' '.join(b) for ind,b in enumerate(books)}
        book_df = pd.DataFrame.from_dict(book_dict, orient = 'index')
        book_df.columns = ['verbose_desc']
        return book_df


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

        # Make a composite description column to be cleaned up
        df['desc_tot'] = df['tags']+' '+ df['title']
        return df

    def assemble_df(self):
        '''
        INPUT: dataframe from gutenberg, podcasts
        OUTPUT: aggregate df
        '''

        #books = pickle.load(open('book_list.pkl'))
        bookdf = self.gutenberg_cat('data/ebooks.csv')

        # Add a clean vectorizable string col to df with raw desc
        bookdf['cleaned_text'] = bookdf['desc_tot'].apply(lambda x: x.split()).apply(self.clean_up)
        bookdf = bookdf[['title_auth', 'cleaned_text']]

        f = open("data/podcast_df.pkl")
        pcast_df = pickle.load(f)
        pcast_df['desc'] = pcast_df['desc'].apply(lambda x: x.split()).apply(self.clean_up)
        #print "Here's a clean dataframe of books: \n", bookdf
        
        bookdf.columns = pcast_df.columns

        # Set media types:
        bookdf['type'] = 'ebook'
        pcast_df['type'] = 'podcast'
        # Set df to bookdf
        self.df = pd.concat([pcast_df, bookdf], axis = 0)



if __name__ == "__main__":

    read = TextParser()
    read.assemble_df()
    print read.df
    quora_user = open('data/quora_data.pkl')
    quora = pickle.load(quora_user)
    filtered = read.preprocess_quora(quora)
    print "Here's some clean Quora data: \n", read.clean_up(filtered)
    

