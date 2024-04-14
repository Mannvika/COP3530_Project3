import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# Replace these values with your own
CLIENT_ID = 'ee38a806ef614c80967d02453cd0c31c'
CLIENT_SECRET = '1723989c8c6d4f1a8c5b6b54ff40d8b3'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_random_tracks(num_tracks, start_year, end_year, min_popularity):
    tracks = []
    total_tracks = 0
    offset = 0
    while total_tracks < num_tracks:
        limit = min(50, num_tracks - total_tracks)
        year = random.randint(start_year, end_year)
        results = sp.search(q=f'year:{year}', type='track', limit=limit, offset=offset, market='US')
        tracks.extend(results['tracks']['items'])
        total_tracks += len(results['tracks']['items'])
        offset += limit
        time.sleep(0.1)

    # Filter tracks by popularity
    filtered_tracks = [track for track in tracks if track['popularity'] >= min_popularity]
    return filtered_tracks



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

    random_tracks = get_random_tracks(100, minimumYear, maximumYear, 5)

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