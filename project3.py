import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# Replace these values with your own
CLIENT_ID = 'ee38a806ef614c80967d02453cd0c31c'
CLIENT_SECRET = '1723989c8c6d4f1a8c5b6b54ff40d8b3'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

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

def main():
    genres = ['pop', 'rock', 'hip hop', 'country', 'jazz', 'k-pop', 'lo-fi', 'metal']

    # Define query variables
    minimumYear = ""
    maximumYear = ""
    songAmount = ""

    # Get and validate input for minimum year from user
    valid_input = False
    while not valid_input:
        minimumYear = input("Enter a minimum year (Between 1970 and 2024) ")
        if minimumYear.isnumeric():
            if 1970 <= int(minimumYear) <= 2024:
                valid_input = True

    # Save it as an int
    minimumYear = int(minimumYear)

    # Get and validate input for maximum year from user
    valid_input = False
    while not valid_input:
        maximumYear = input("Enter a maximum year (Between 1970 and 2024) ")
        if maximumYear.isnumeric():
            if minimumYear <= int(maximumYear) <= 2024:
                valid_input = True

    # Save it as an int
    maximumYear = int(maximumYear)

    # Get and validate input for song number from user
    valid_input = False
    while not valid_input:
        songAmount = input("Enter number of songs (Between 30 and 50) ")
        if songAmount.isnumeric():
            if 30 <= int(songAmount) <= 50:
                valid_input = True

    # Save it as an int
    songAmount = int(songAmount)

    print("Generating Playlist...")

    random_tracks = get_random_songs_from_playlist("6yPiKpy7evrwvZodByKvM9", songAmount)
    print(getGenre(random_tracks[0]))

    track_index_map = {}
    for i, track in enumerate(random_tracks):
        track_index_map[i] = track

    #print(track_index_map[0])

    graph = [[1000]*len(random_tracks) for i in range(len(random_tracks))]
    print(graph)

    #for i in range(len(graph)):
        #for j in range(len(graph[i])):

if __name__ == "__main__":
    main()