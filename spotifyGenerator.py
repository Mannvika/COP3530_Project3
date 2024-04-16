import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time
from graph import Graph


class SpotifyGenerator:

    def __init__(self, playlist_id, subset_amount):

        # Connect to spotify API, and generate spotipy object
        client_credentials_manager = SpotifyClientCredentials(client_id='ee38a806ef614c80967d02453cd0c31c', client_secret='1723989c8c6d4f1a8c5b6b54ff40d8b3')
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        self.subset_amount = subset_amount

        # Get a random subset of songs from the playlist
        self.playlist = self.get_random_songs_from_playlist(playlist_id)

        # Save a dictionary of the overall genres, each vertex's genre list, and each track's index
        self.overall_genres = {}
        self.vertex_genre_map = {}
        self.track_index_map = {}

        # Build the track index
        self.build_track_index_map()

        # Build the graph
        self.graph = self.build_graph()

        # Save a list of the acceptable genres (genres that have the requested amount of tracks)
        self.acceptable_genres = []
        self.selected_genre = ""

    def get_random_songs_from_playlist(self, playlist_id):
        # Offset refers to the index to start from
        offset = 0

        # Save a list of the songs we get
        playlist_tracks = []

        print("Getting Songs...")

        # While we have less than subset_amount * 4 songs in our playlist_tracks
        while len(playlist_tracks) < (self.subset_amount * 4):

            # Get 100 items, add it to the playlist_tracks, and then move offset by the length of items we got
            results = self.sp.playlist_items(playlist_id, limit=100, offset=offset)
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
        selected_tracks = random.sample(playlist_tracks, min(self.subset_amount, len(playlist_tracks)))

        print("Finished Getting Songs...")
        return selected_tracks

    def get_genre(self, track, index):
        # Get the name of the artist
        artist_name = track['track']['artists'][0]['name']

        # If this returns a non-empty value, get the artist object
        if artist_name != '':
            artist_info = self.sp.search(q=artist_name, type='artist')
        # Otherwise ignore this track
        else:
            self.vertex_genre_map[index] = []
            return []

        # Get all the genres of this artist
        genres = artist_info['artists']['items'][0]['genres']

        # For each of these genres either add it to the map, or increase the frequency
        for genre in genres:
            if genre in self.overall_genres:
                self.overall_genres[genre] += 1
            else:
                self.overall_genres[genre] = 1

        # Save this vertices genre list so we don't have to make api calls to find it again
        self.vertex_genre_map[index] = genres
        return genres

    def build_track_index_map(self):
        # Map each song to an index
        for i, track in enumerate(self.playlist):
            self.track_index_map[i] = track
            self.get_genre(track, i)

    def build_graph(self):
        # Create a nxn matrix, where n is the number of random songs we got
        graph = [[1000] * len(self.playlist) for i in range(len(self.playlist))]

        # Create a graph, where the edges represent 1000 - the number of shared genres
        for i in range(len(graph)):
            for j in range(len(graph[i])):
                if i != j:
                    graph[i][j] = graph[i][j] - len(set(self.vertex_genre_map[i]) & set(self.vertex_genre_map[j]))

        # Create graph object
        g = Graph(graph, len(self.playlist))
        return g

    def print_acceptable_genres(self, song_amount):
        # Reset acceptable genres
        self.acceptable_genres = []

        # For each genre, if there are enough tracks that we are able to create a playlist from it then save it
        for key in self.overall_genres:
            if self.overall_genres[key] >= song_amount:
                self.acceptable_genres.append(key)

        # Print these genre options to the user
        for i, genre in enumerate(self.acceptable_genres):
            self.acceptable_genres[i] = genre
            print(i, ". ", genre)

    def select_genre(self, index):
        # Select the genre based on user index
        self.selected_genre = self.acceptable_genres[index]

    def print_tracks(self, song_amount):

        # Get a starting vertex by finding the first instance of that genre in our graph
        starting_vertex = 0
        for i in range(len(self.vertex_genre_map)):
            genres = self.vertex_genre_map[i]
            found = False
            for genre in genres:
                if genre == self.selected_genre:
                    starting_vertex = i
                    found = True
                    break
            if found:
                break

        # Find the most similar songs from our graph
        song_indices = self.graph.dijkstras(self.subset_amount, song_amount, starting_vertex)

        # Print the songs and their links
        print("Your songs are: ")
        for i in song_indices:
            name = self.track_index_map[i]['track']['name']
            url = self.track_index_map[i]['track']['external_urls']['spotify']
            print(name + ": " + url)

