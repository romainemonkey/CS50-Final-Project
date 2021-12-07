from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from spotify import dothings
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        if dothings() == 0:
            return render_template('failure.html')
        else:


@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

if __name__ == "__main__":
    app.run(debug=True)