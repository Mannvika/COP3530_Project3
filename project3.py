import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

CLIENT_ID = 'ee38a806ef614c80967d02453cd0c31c'
CLIENT_SECRET = '1723989c8c6d4f1a8c5b6b54ff40d8b3'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_genre(track):
    track_info = track['track']
    artist_ids = [artist['id'] for artist in track_info['artists']]
    artists = sp.artists(artist_ids)['artists']
    genres = []
    for artist in artists:
        genres.extend(artist['genres'])
    return genres


def get_random_songs_from_playlist(playlist_id, subset_amount):
    offset = 0
    playlist_tracks = []

    print("Getting Songs...")
    while len(playlist_tracks) < (subset_amount * 4):
        results = sp.playlist_items(playlist_id, limit=100, offset=offset)
        items = results['items']
        playlist_tracks.extend(items)

        offset += len(items)

        if len(items) < 100:
            break
        time.sleep(0.01)

    random.shuffle(playlist_tracks)

    selected_tracks = random.sample(playlist_tracks, min(subset_amount, len(playlist_tracks)))

    print("Finished Getting Songs...")
    return selected_tracks


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

    random_tracks = get_random_songs_from_playlist("6yPiKpy7evrwvZodByKvM9", 400)

    print("Generating Map...")
    track_index_map = {}
    for i, track in enumerate(random_tracks):
        track_index_map[i] = track

    print("Generating Graph...")

    graph = [[1000]*len(random_tracks) for i in range(len(random_tracks))]

    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if i != j:
                graph[i][j] = graph[i][j] - len(set(get_genre(track_index_map[i]))&set(get_genre(track_index_map[j])))
                print(get_genre(track_index_map[i]))


if __name__ == "__main__":
    main()
