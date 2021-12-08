from flask import Flask, render_template, request
import sqlite3
import numpy
import random
import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
from spotify import getCache
import webbrowser

# sets important global variables
cid = "9034fffac585493e8a505eb5fbaf7570"
secret = "820f38bbb98f4651aa4eb7c606322f68"
reduri = "https://google.com"
app = Flask(__name__)

# opens the web browser
webbrowser.open('http://localhost:5000/')

# flask object for the home page and function of the website
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        os.environ['SPOTIPY_CLIENT_ID']= cid
        os.environ['SPOTIPY_CLIENT_SECRET']= secret
        os.environ['SPOTIPY_REDIRECT_URI']=reduri

        print("i love harvard university")


        # establishes user and spotipy information, which is needed to get the user's token
        username = ""
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        scope = 'user-top-read'
        token = util.prompt_for_user_token(username, scope)

        if token:
            sp = spotipy.Spotify(auth=token)
        else:
            print("Can't get token for", username)
        # get user token
        token = util.prompt_for_user_token(username,
                scope,
                client_id=cid,
                client_secret=secret,
                redirect_uri=reduri)

        if token:
            sp = spotipy.Spotify(auth=token)
            # extracts the user's top 50 songs on spotify from the last 6 months
            results = sp.current_user_top_tracks(limit=50,offset=0,time_range='medium_term')
            # appends each result to a json file, from which the data will be properly extracted
            for song in range(50):
                songlist = []
                songlist.append(results)
                with open('top50_data.json', 'w', encoding='utf-8') as f:
                    json.dump(songlist, f, ensure_ascii=False, indent=4)

            # the following lines of code sort the pieces of data from the user's top tracks into arrays
            with open('top50_data.json', encoding='utf-8') as f:
                data = json.load(f)
                listOfResults = data[0]["items"]
                artistNames = []
                songNames = []
                URIs = []
                for result in listOfResults:
                    artistName = result["artists"][0]["name"]
                    artistNames.append(artistName)
                    songName = result["name"]
                    songNames.append(songName)
                    URI = result["uri"]
                    URIs.append(URI)
        else:
            print("error 3")
            return render_template ('failure.html')

        # establish the cursor through which to extract data from test.db
        sqliteConnect = sqlite3.connect("test.db")
        cursor = sqliteConnect.cursor()
        genres = {}
        meanPop = 0
        # go through the artists, search for their associated genres, and then compile a dictionary
        # genre : # of times that genre appears in the user's top track's artists
        for name in artistNames:
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            result = sp.search(name)
            track = result['tracks']['items'][0]

            artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])

            if (artist["genres"] != []):
                for genre in artist["genres"]:
                    if genre in genres.keys():
                        genres[genre] += 1
                    else:
                        genres[genre] = 1
            meanPop += artist["popularity"]

        #calculate the average popularity, a metric determined by spotify, of the user's artists
        meanPop = meanPop/50

        sortedGenres = dict(sorted(genres.items(), key = lambda kv: kv[1]))
        


        # more determining of a module for sqlite3 use
        sqliteConnect = sqlite3.connect("test.db")
        cursor = sqliteConnect.cursor()
        comments = []



        # add comments based on mean popularity of songs, drawing from a predetermined table in test.db
        popCheck = 10 * round(meanPop/10)
        print("popCheck: " + str(popCheck))
        if popCheck < 40:
            popCheck = 40
        if popCheck in [40, 50, 60, 70, 80, 90, 100]:
            query = """SELECT * FROM popcoms WHERE range = "{}" """.format(popCheck)
            data = cursor.execute(query).fetchall()
            comments.append("@#Benjy: #@" + data[0][2])
            comments.append("@#Will: #@" + data[0][1])


        uniqueArtists = set(artistNames)
        uniqueArtists = list(uniqueArtists)
        # syntax:      !@artist@!   @#commenter: #@

        # add comments based on individual artists, drawing from a predetermined table in test.db
        for artist in uniqueArtists:
            query = """SELECT benjy FROM artcoms WHERE artist = "{}" """.format(artist.lower())
            data = cursor.execute(query).fetchall()
            if data != [(u'',)] and data != [] and data != [(None,)]:
                comments.append("@#Benjy: #@" + data[0][0])
            query = """SELECT will FROM artcoms WHERE artist = "{}" """.format(artist.lower())
            data = cursor.execute(query).fetchall()
            if data != [(u'',)] and data != [] and data != [(None,)]:
                comments.append("@#Will: #@" + data[0][0])

        # these comments are random comments, with FILL IN THE BLANK type syntax
        query = """SELECT * FROM rancoms"""
        rancoms = cursor.execute(query).fetchall()
        randartno = 5

        # picks randartno random numbers from 0 to the number of unique artists in the user's top tracks
        randarts = random.sample(list(numpy.linspace(0,len(uniqueArtists)-1,len(uniqueArtists))),randartno)

        # adds the random comments, filling in the blanks where ARTISTNAME exists
        randids = random.sample(list(numpy.linspace(0,len(rancoms)-2,len(rancoms)-1)),randartno)
        for i in range(len(randids)):
            if rancoms[int(randids[i])+1][2]:
                newcomment = rancoms[int(randids[i])+1][2]
                newcomment = newcomment.replace("ARTISTNAME",uniqueArtists[int(randarts[i])])
                newcomment = "@#Benjy: #@" + newcomment
                comments.append(newcomment)
            elif rancoms[int(randids[i])+1][1]:
                newcomment = rancoms[int(randids[i])+1][1]
                newcomment = newcomment.replace("ARTISTNAME",uniqueArtists[int(randarts[i])])
                newcomment = "@#Will: #@" + newcomment
                comments.append(newcomment)

        # close the cursor
        sqliteConnect.close()

        # return and render the results page with said comments
        vals = random.sample(comments,len(comments))
        return render_template('results.html',vals=vals)

# deal with this benjy
@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

if __name__ == "__main__":
    app.run(debug=False)
