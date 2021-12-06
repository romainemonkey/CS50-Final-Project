import os
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util

cid = "28832d036d4341d68dc4acea6dfc94b5"
secret = "f810bd1fc2d3423d8009b28470cb7024"

os.environ['SPOTIPY_CLIENT_ID']= cid
os.environ['SPOTIPY_CLIENT_SECRET']= secret
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:8888/callback'

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
    print("hello")
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
    print(songNames)
    print(artistNames)

    
else:
    print("Can't get token for", username)


 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
result = sp.search("Ricky Montgomery")
track = result['tracks']['items'][0]

artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
print("artist genres:", artist["genres"][0])