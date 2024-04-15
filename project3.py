import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time
import sys

CLIENT_ID = 'ee38a806ef614c80967d02453cd0c31c'
CLIENT_SECRET = '1723989c8c6d4f1a8c5b6b54ff40d8b3'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_genre(track):
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

# Dijkstras Algorithm: https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/
def dijkstras_shortest_path(graph, source, num_of_songs):

    vs = {}
    s = {}
    dimensions = []
    predecessors = []

    for i in range(len(graph)):
        vs.add(i)
        dimensions[i] = sys.maxsize
        predecessors[i] = -1



    return False


def main():
    song_amount = ""

    # Get and validate input for song number from user
    valid_input = False
    while not valid_input:
        song_amount = input("Enter number of songs (Between 30 and 50) ")
        if song_amount.isnumeric():
            if 5 <= int(song_amount) <= 50:
                valid_input = True

    # Save it as an int
    song_amount = int(song_amount)

    print("Generating Playlist...")

    random_tracks = get_random_songs_from_playlist("6yPiKpy7evrwvZodByKvM9", 317)
    track_index_map = {}
    for i, track in enumerate(random_tracks):
        track_index_map[i] = track

    graph = [[1000]*len(random_tracks) for i in range(len(random_tracks))]

    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if i != j:
                graph[i][j] = graph[i][j] - len(set(get_genre(track_index_map[i]))&set(get_genre(track_index_map[j])))


if __name__ == "__main__":
    main()
