from flask import Flask, render_template, request
from spotify import dothings
import sqlite3
import numpy

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        vals = dothings()
        print(vals)

        if vals == 0 or vals == 1:
            return render_template('failure.html')
        else:
            vals = numpy.transpose(vals)
            print(vals)
            return render_template('results.html',vals=vals)

# deal with this benjy
@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

if __name__ == "__main__":
    app.run(debug=True)