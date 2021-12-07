from flask import Flask, render_template, request
#from spotify import dothings
import sqlite3

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')
    # if request.method == "GET":
    #     return render_template('index.html')
    # elif request.method == "POST":
    #     if dothings() == 0:
    #         return render_template('failure.html')


@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

if __name__ == "__main__":
    app.run(debug=True)