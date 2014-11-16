from flask import Flask
from flask import render_template
import pandas as pd
import pickle
from quora_scrape import profile_crawl
app = Flask(__name__)

# Load dataframe of recommendations
df = pickle.load(open("../data/recs.pkl", "rb"))
df['div_tag'] = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE']

@app.route('/recs')
def index():
    return render_template('index.html', data = df[['title', 'img_link', 'div_tag']].values)


@app.route('/')
def submit_quora():
	return render_template('submit.html')


@app.route('/recommend', methods=['POST'])
def recommend():
	user_data = str(request.form['user_input'])
	profile_crawl(user_data)
	df = main()
	return render_template('index.html', data = df['img_link'].values)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7777, debug=True)
