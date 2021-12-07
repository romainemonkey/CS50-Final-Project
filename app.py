from flask import Flask, render_template, request
from spotify import dothings
import sqlite3
import numpy
import random
import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
import math

cid = "28832d036d4341d68dc4acea6dfc94b5"
secret = "f810bd1fc2d3423d8009b28470cb7024"

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        print("hello1")
        return render_template('index.html')
    elif request.method == "POST":
        print("hello2")

        os.environ['SPOTIPY_CLIENT_ID']= cid
        os.environ['SPOTIPY_CLIENT_SECRET']= secret
        os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:5000/'

        print("i love harvard university")

        username = ""
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

        try:
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        except:
            print("error 0")
            return render_template('failure.html')
        scope = 'user-top-read'
        try:
            token = util.prompt_for_user_token(username, scope)
        except:
            print("error 1")
            return render_template('failure.html')

        print(token)

        if token:
            sp = spotipy.Spotify(auth=token)
            results = sp.current_user_top_tracks(limit=50,offset=0,time_range='medium_term')
            for song in range(50):
                songlist = []
                songlist.append(results)
                with open('top50_data.json', 'w', encoding='utf-8') as f:
                    json.dump(songlist, f, ensure_ascii=False, indent=4)
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

        sqliteConnect = sqlite3.connect("test.db")
        cursor = sqliteConnect.cursor()
        genres = {}
        meanPop = 0
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

        meanPop = meanPop/50

        sortedGenres = dict(sorted(genres.items(), key = lambda kv: kv[1]))
        


        # artist test by benjy
        sqliteConnect = sqlite3.connect("test.db")
        cursor = sqliteConnect.cursor()
        comments = []



        # add comments based on mean popularity of songs
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

        for artist in uniqueArtists:
            query = """SELECT benjy FROM artcoms WHERE artist = "{}" """.format(artist.lower())
            data = cursor.execute(query).fetchall()
            if data != [(u'',)] and data != [] and data != [(None,)]:
                comments.append("@#Benjy: #@" + data[0][0])
            query = """SELECT will FROM artcoms WHERE artist = "{}" """.format(artist.lower())
            data = cursor.execute(query).fetchall()
            if data != [(u'',)] and data != [] and data != [(None,)]:
                comments.append("@#Will: #@" + data[0][0])


        query = """SELECT * FROM rancoms"""
        rancoms = cursor.execute(query).fetchall()
        randartno = 5

        randarts = random.sample(list(numpy.linspace(0,len(uniqueArtists)-1,len(uniqueArtists))),randartno)

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

        print(comments)
        sqliteConnect.close()

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
    app.run(debug=True)