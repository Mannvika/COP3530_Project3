import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# Replace these values with your own
CLIENT_ID = 'ee38a806ef614c80967d02453cd0c31c'
CLIENT_SECRET = '1723989c8c6d4f1a8c5b6b54ff40d8b3'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)