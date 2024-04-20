import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time


CLIENT_ID = '56fd7a0ba572466cb89ad2fb8720ff6f'
CLIENT_SECRET = '4443915226de4419985f628fbaef79e4'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_genre(track):
    # Get the name of the artist
    artist_name = track['track']['artists'][0]['name']

    # If this returns a non-empty value, get the artist object
    if artist_name != '':
        artist_info = sp.search(q=artist_name, type='artist')
    # Otherwise ignore this track
    else:
        return []

    # Get all the genres of this artist
    genres = artist_info['artists']['items'][0]['genres']

    # Save this vertices genre list so we don't have to make api calls to find it again
    return genres


def get_random_songs_from_playlist(playlist_id, subset_amount):
    # Offset refers to the index to start from
    offset = 0

    # Save a list of the songs we get
    playlist_tracks = []

    print("Getting Songs...")

    # While we have less than subset_amount * 4 songs in our playlist_tracks
    while len(playlist_tracks) < (subset_amount * 4):

        # Get 100 items, add it to the playlist_tracks, and then move offset by the length of items we got
        results = sp.playlist_items(playlist_id, limit=100, offset=offset)
        items = results['items']
        playlist_tracks.extend(items)

        offset += len(items)

        # If we have less than 100 items, we've reached the end of the playlist
        if len(items) < 100:
            break

        # Sleep to prevent api from hitting the rate limit
        time.sleep(0.01)

    # Get a subset amount of random songs from the playlist tracks
    random.shuffle(playlist_tracks)
    selected_tracks = random.sample(playlist_tracks, min(subset_amount, len(playlist_tracks)))

    print("Finished Getting Songs...")
    return selected_tracks


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



