from flask import Flask
from flask import render_template
import pandas as pd
import pickle
from quora_scrape import profile_crawl
app = Flask(__name__)

# Load dataframe of recommendations
df = pickle.load(open("../data/recs.pkl", "rb"))

@app.route('/')
def index():
    return render_template('index.html', data = df[['title', 'img_link']].values)


@app.route('/quora_submit')
def submit_quora():
	return '''
	
	<br>
	Please enter your Quora profile page URL here:
	<br>

	<form action="/recommend" method = 'POST'>
		<input type="text" name = 'user_input'>
		<input type = "submit" />
	'''

@app.route('/recommend', methods=['POST'])
def recommender():
	user_data = str(request.form['user_input'])
	profile_crawl(user_data)
	df = main()
	return render_template('index.html', data = df['img_link'].values)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7777, debug=True)
