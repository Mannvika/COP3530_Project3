import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time


CLIENT_ID = '56fd7a0ba572466cb89ad2fb8720ff6f'
CLIENT_SECRET = '4443915226de4419985f628fbaef79e4'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def getGenre(track):
    #Returns a list of genres for each tarck we get from spotify
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


class Song:
    #Song object that contains information that we will output
    def __init__(self, title, url, genres):
        self.title = title
        self.genres = genres
        self.url = url





class HashMap:
    def __init__(self, size):
        self.size = size
        self.map = [[] for _ in range(size)] #List of list of tuples of (genre, song)
        self.gen_list = [] #Contains list of all genres

    def hash_function(self, genre): #Hashing the genre.
        hash_value = 0
        for char in genre:
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value

    def insert(self, song): #Finding a bucket and inserting the (genre, song) tuple
        for genre in song.genres:   #[(pop, song1), (pop, song2)]
            index = self.hash_function(genre)
            self.map[index].append((genre, song))
            if genre not in self.gen_list:
                self.gen_list.append(genre) #Using separate chaining for collisions


    def search(self, genre): #To search, go to the specific bucket that will contain the genre, and return songs of that genre
        index = self.hash_function(genre)
        results = []
        if not self.map[index]:
            return "Empty" #If the bucket is empty then that genre is not present
        for key, value in self.map[index]:
            if key == genre:
                results.append(value)
        return results



