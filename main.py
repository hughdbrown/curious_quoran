from recommend import Recommender
from parser import TextParser
import pickle


def main():
    '''
    INPUT: None
    OUTPUT: Recommendations sorted in order of relevance
    
    Uses the TextParer and Recommender classes to generate resource recommendations given a user's Quora data
    '''

    read = TextParser()
    read.assemble_df()
    print read.df
    pickle.dump(read.df, open("data/master_df.pkl", "wb"))
    quora_user = open('data/quora_data.pkl')
    quora = pickle.load(quora_user)
    filtered = read.preprocess_quora(quora)
    clean_quora = read.clean_up(filtered)
    print "Here's your clean Quora data: \n", clean_quora
    pickle.dump(clean_quora, open("data/clean_quora.pkl", "wb"))

    # Make recommendations
    rec = Recommender()
    test = rec.vectorize()
    top_ten_ind = rec.recommend()
    recs = read.df.ix[top_ten_ind]
    print "These are your recommendations: \n"
    print recs[['title', 'type']]

if __name__ =="__main__":
	main()	