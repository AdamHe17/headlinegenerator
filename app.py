import random
import time

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index(dynamic=random.random()):
    return render_template('index.html', dynamic=dynamic)


@app.route('/analysis', methods=['POST'])
def analysis(dynamic=random.random()):
    article = request.form['article']
    time.sleep(7)
    return render_template('analysis.html', article=article, dynamic=dynamic, headlines=['test headline 1', 'test headline 2'])

if __name__ == "__main__":
    app.run(debug=True)
