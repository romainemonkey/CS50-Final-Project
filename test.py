import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
import os

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
    print("error 0")
    exit()
scope = 'user-top-read'
try:
    token = util.prompt_for_user_token(username, scope)
except:
    print("error 1")
    exit()
print(token)

sp = spotipy.Spotify(auth=token)
results = sp.current_user_top_tracks(limit=50,offset=0,time_range='medium_term')
print(results)