import os
import json
import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util

cid = "28832d036d4341d68dc4acea6dfc94b5"
secret = "f810bd1fc2d3423d8009b28470cb7024"

os.environ['SPOTIPY_CLIENT_ID']= cid
os.environ['SPOTIPY_CLIENT_SECRET']= secret
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:5000'

print("i love harvard university")

username = ""
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
scope = 'user-top-read'
token = util.prompt_for_user_token(username, scope)

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

# sqlCommand = """CREATE TABLE temp ( 
# artist_name STRING,
# genres STRING,
# popularity INT
# );"""

# cursor.execute(sqlCommand)

for name in artistNames:
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    result = sp.search(name)
    track = result['tracks']['items'][0]

    artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])

    genres = ""
    if (artist["genres"] != []):
        for genre in artist["genres"]:
            genres = genres + "|" + genre
    # print(name)
    # print(genres)
    # print(artist["popularity"])
    sqlCommand = """INSERT INTO temp VALUES ("{name}", "{genres}", {popularity})""".format(name=name, genres=genres, popularity=artist["popularity"])
    cursor.execute(sqlCommand)
query = """SELECT * FROM temp"""
fetch = cursor.execute(query)
# print(fetch.fetchall())

print(fetch.fetchall()[0])
sqliteConnect.close()