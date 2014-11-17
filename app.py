from flask import Flask, request, render_template
import pandas as pd
import pickle
from recommend import Recommender
from parser import TextParser
from image_scraper import get_image
from quora_scrape import profile_crawl
app = Flask(__name__)

# Load dataframe of pre-made recommendations for testing purposes, add a div tag col for rendering on the page
# df = pickle.load(open("data/recs.pkl", "rb"))
# df['div_tag'] = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE']


# Load in all the pickled files needed for recommending
# fit_vec = pickle.load(open('../data/vectorizer.pkl'))
# docs_mat = pickle.load(open('../data/vectorized_docs.pkl'))
master_df = pickle.load(open('data/master_df.pkl'))


@app.route('/')
def submit_quora():
	return render_template('submit.html')

@app.route('/recommend', methods=['POST'])
def recommend():
	user_data = str(request.form['user_input'].encode('utf-8'))

	# --- Drive to the given URL, scrape and generate recs -- #
	scraped = profile_crawl(user_data)
	quora = scraped['text']
	
	# Read and clean Quora dump recommendations
	read = TextParser()
	read.df = master_df
	filtered = read.preprocess_quora(quora)
	clean_quora = read.clean_up(filtered)
	pickle.dump(clean_quora, open("data/clean_quora.pkl", "wb"))
	rec = Recommender()
	test = rec.vectorize()
	top_ten_ind = rec.recommend()
	recs = read.df.ix[top_ten_ind]
	recs = recs.reset_index()
	recs['img_link'] = map(get_image, recs['title'])
	recs.loc[recs['type']=='course', 'img_link'] = 'http://www.michaellenox.com/wp-content/uploads/2014/07/coursera_square_logo.jpg'
	recs = recs[0:5]
	recs['div_tag'] = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE']
	return render_template('index.html', data = recs[['title', 'img_link', 'div_tag']].values)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7724, debug=True)
