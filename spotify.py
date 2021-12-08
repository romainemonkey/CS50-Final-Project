import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

def getCache():
    cid = "28832d036d4341d68dc4acea6dfc94b5"
    secret = "f810bd1fc2d3423d8009b28470cb7024"

    os.environ['SPOTIPY_CLIENT_ID']= cid
    os.environ['SPOTIPY_CLIENT_SECRET']= secret
    os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:5000/callback'

    username = ""
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    scope = 'user-top-read'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_top_tracks(limit=50,offset=0,time_range='medium_term')
    else:
        print("Can't get token for", username)

getCache()

if __name__ == "__main__":
    getCache()