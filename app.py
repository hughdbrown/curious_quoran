from flask import Flask
from flask import render_template
import pandas as pd
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
