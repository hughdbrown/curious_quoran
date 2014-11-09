import recommend
import parser


def main():
	'''
	INPUT: None
	OUTPUT: Top ten recommendations

	Uses parser and recommendation classes to generate recommendations with cosine similarity
	'''

	read = TextParser()
	read.assemble_df()
	print read.df
	quora_user = open('data/quora_data.pkl')
	quora = pickle.load(quora_user)
	filtered = read.preprocess_quora(quora)
	print "Here's some clean Quora data: \n", read.clean_up(filtered)

	rec = Recommender()
	top_ten_ind = rec.recommend()
	recs = read.df.ix[top_ten_ind]
	return recs[['title', 'type']]


if __name__ =="__main__:
	main()	