import os
import json
import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
import numpy
import random


def dothings():
    cid = "28832d036d4341d68dc4acea6dfc94b5"
    secret = "f810bd1fc2d3423d8009b28470cb7024"

    os.environ['SPOTIPY_CLIENT_ID']= cid
    os.environ['SPOTIPY_CLIENT_SECRET']= secret
    os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:5000/'

    print("i love harvard university")

    username = ""
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    try:
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except:
        return 0
    scope = 'user-top-read'
    try:
        token = util.prompt_for_user_token(username, scope)
    except:
        return 0

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_top_tracks(limit=50,offset=0,time_range='medium_term')
        for song in range(50):
            list = []
            list.append(results)
            with open('top50_data.json', 'w', encoding='utf-8') as f:
                json.dump(list, f, ensure_ascii=False, indent=4)
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
        print("Can't get token for", username)
        # todo: render_template ('failure.html')

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
    print(meanPop)
    print(artistNames)
    print(songNames)
    sortedGenres = dict(sorted(genres.items(), key = lambda kv: kv[1]))
    print(sortedGenres)
    


    # artist test by benjy
    comments = []
    authors = []


    uniqueArtists = list(set(artistNames))
    for artist in uniqueArtists:
        query = "SELECT benjy FROM artcoms WHERE artist = ?", artist.lower()
        data = cursor.execute(query).fetchall()
        bcheck = data[0][0]
        if len(bcheck) != 0:
            comments.append(bcheck)
            authors.append("Benjy")
        query = "SELECT will FROM artcoms WHERE artist = ?", artist.lower()
        data = cursor.execute(query).fetchall()
        wcheck = data[0][0]
        if len(wcheck) != 0:
            comments.append(wcheck)
            authors.append("will")

    query = "SELECT * FROM rancoms"
    data = cursor.execute(query).fetchall()
    rancoms = data[0]
    randartno = 3
    randids = random.sample(numpy.linspace(0,len(rancoms)-1,len(rancoms)),randartno)
    for i in range(len(randids)):
        if rancoms[randids[i]]["benjy"]:
            comments.append(rancoms[randids[i]]["benjy"])
            authors.append("Benjy")
        elif rancoms[randids[i]]["will"]:
            comments.append(rancoms[randids[i]]["will'"])
            authors.append("Will")

    command = """INSERT INTO temp VALUES ("hello", "hello", 1)"""
    cursor.execute(command)

    query = """SELECT * FROM temp"""
    data = cursor.execute(query).fetchall()
    print(data)



    sqliteConnect.close()
    return 1
    

dothings()