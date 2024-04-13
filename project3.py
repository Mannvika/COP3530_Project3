import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# Replace these values with your own
CLIENT_ID = 'ee38a806ef614c80967d02453cd0c31c'
CLIENT_SECRET = '1723989c8c6d4f1a8c5b6b54ff40d8b3'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_random_tracks(num_tracks, start_year, end_year):
    tracks = []
    total_tracks = 0
    offset = 0
    while total_tracks < num_tracks:
        limit = min(50, num_tracks - total_tracks)
        year = random.randint(start_year, end_year)
        results = sp.search(q=f'year:{year}', type='track', limit=limit, offset=offset, market='US')
        total_tracks += len(results['tracks']['items'])
        tracks.extend(results['tracks']['items'])
        offset += limit
        time.sleep(0.1)
    return tracks

def main():
    genres = ['pop', 'rock', 'hip hop', 'country', 'jazz', 'k-pop', 'lo-fi', 'metal']

    minimumYear = int(input("Enter a minimum year (Between 1970 and 2024) "))
    maximumYear = int(input("Enter a maximum year (Between 1970 and 2024) "))
    songAmount = int(input("Enter number f songs"))

    print("Generating Playlist")

    random_tracks = get_random_tracks(500, minimumYear, maximumYear)

    track_index_map = {}
    for i, track in enumerate(random_tracks):
        track_index_map[i] = track

    graph = [[1000]*len(random_tracks) for i in range(len(random_tracks))]
    print(graph)

    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if i != j:
                #comparison



if __name__ == "__main__":
    main()