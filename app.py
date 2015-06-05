from __future__ import print_function

import pickle

from flask import Flask, request, render_template
import pandas as pd

from recommend import Recommender
from parser import TextParser
from image_scraper import get_image
from quora_scrape import profile_crawl

app = Flask(__name__)

with open("data/recs.pkl", "rb") as f:
	df = pickle.load(f)
with open('data/master_df.pkl') as f:
	master_df = pickle.load(f)

@app.route('/')
def submit_quora():
	return render_template('submit.html')

@app.route('/test')
def rec():	
	return render_template('testing.html', data = df[['title', 'img_link']].values)


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
	with open("data/clean_quora.pkl", "wb") as f:
		pickle.dump(clean_quora, f)
	rec = Recommender()
	test = rec.vectorize()
	top_ten_ind = rec.recommend()
	recs = read.df.ix[top_ten_ind]
	recs = recs.reset_index()
	recs['img_link'] = map(get_image, recs['title'])
	recs.loc[recs['type']=='course', 'img_link'] = 'http://www.michaellenox.com/wp-content/uploads/2014/07/coursera_square_logo.jpg'
	recs = recs[0:20] # Get the top twenty recommendations
	return render_template('testing.html', data = recs[['title', 'img_link']].values)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8321, debug=True)
