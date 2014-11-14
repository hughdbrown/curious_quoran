from flask import Flask
from flask import render_template
import pandas as pd
import pickle
app = Flask(__name__)


df = pickle.load(open("data/recs.pkl", "rb"))

@app.route('/')
def index():
    return render_template('index.html', data = df['img_link'].values)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
