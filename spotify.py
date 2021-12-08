import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

def getCache():
    cid = "9034fffac585493e8a505eb5fbaf7570"
    secret = "820f38bbb98f4651aa4eb7c606322f68"

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