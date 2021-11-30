import os
import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth

cid = "28832d036d4341d68dc4acea6dfc94b5"
secret = "f810bd1fc2d3423d8009b28470cb7024"

os.environ['SPOTIPY_CLIENT_ID']= cid
os.environ['SPOTIPY_CLIENT_SECRET']= secret
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:8888/callback'

print("i love harvard university")