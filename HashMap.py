import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time


CLIENT_ID = 'ee38a806ef614c80967d02453cd0c31c'
CLIENT_SECRET = '1723989c8c6d4f1a8c5b6b54ff40d8b3'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class Song:
    def __init__(self, title, genres):
        self.title = title
        self.genres = genres

def getGenre(track):
    artist_ids = [artist['id'] for artist in track['artists']]
    artists = sp.artists(artist_ids)['artists']
    genres = []
    for artist in artists:
        genres.extend(artist['genres'])
    return genres

def get_random_songs_from_playlist(playlist_id, n):

    # Fetch playlist tracks
    playlist_tracks = sp.playlist_items(playlist_id)['items']

    # Extract track IDs
    track_ids = [track['track']['id'] for track in playlist_tracks if
                 track['track'] is not None and track['track']['id'] is not None]

    # Randomly select n tracks
    selected_tracks = random.sample(track_ids, min(n, len(track_ids)))

    # Fetch track details
    random_songs = []
    for track_id in selected_tracks:
        # Handle rate limiting
        while True:
            try:
                track_info = sp.track(track_id)
                random_songs.append(track_info)
                break
            except spotipy.SpotifyException as e:
                if e.http_status == 429:  # Rate limiting, wait and retry
                    time.sleep(5)  # Wait for 5 seconds and retry
                else:
                    print("Error fetching track:", e)
                    break

    return random_songs




class HashMap:
    def __init__(self, size):
        self.size = size
        self.map = [[] for _ in range(size)]
        self.gen_list = []

    def hash_function(self, genre):
        hash_value = 0
        for char in genre:
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value

    def insert(self, song):
        for genre in song.genres:   #[(pop, song1), (pop, song2)]
            index = self.hash_function(genre)
            self.map[index].append((genre, song))
            if genre not in self.gen_list:
                self.gen_list.append(genre)


    def search(self, genre):
        index = self.hash_function(genre)
        results = []
        if not self.map[index]:
            return "Empty"
        for key, value in self.map[index]:
            if key == genre:
                results.append(value.title)
        return results



