import os
import random
import time

import linguistics
import microsoft
from flask import Flask, render_template, request
from newspaper import Article

app = Flask(__name__)


@app.route('/')
def index(dynamic=random.random()):
    return render_template('index.html', dynamic=dynamic)


@app.route('/analysis', methods=['POST'])
def analysis(dynamic=random.random()):
    article = request.form['article']
    time.sleep(2)
    phrases = microsoft.get_key_phrases(article)
    clusters = microsoft.find_clusters(phrases, article)
    return render_template('analysis.html', article=article, dynamic=dynamic, headlines=[linguistics.headline(clusters, 10)])

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
