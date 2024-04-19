from HashMap import HashMap
from HashMap import Song
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time
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

    songs = get_random_songs_from_playlist("6yPiKpy7evrwvZodByKvM9", 350)

    hash_map = HashMap(50)

    for i in range(len(songs) - 1):
        song = Song(songs[i]['name'], getGenre(songs[i]))
        hash_map.insert(song)


    song_number = int(input("Enter number of songs for playlist (between 1 and 25):"))

    for i in range(len(hash_map.gen_list)-1):
        print(f'{i}. {hash_map.gen_list[i]}')


    index = int(input("Enter index of desired genre: "))



    final = hash_map.search(hash_map.gen_list[index])
    while len(final) < song_number:
        ind = int(input('Not enough songs in genre, enter another index:'))
        a=hash_map.search(hash_map.gen_list[ind])
        for item in a:
            if item not in final:
                final.append(item)

        #final.extend(hash_map.search(hash_map.gen_list[ind]))







    for i in range(song_number):
        print(f'{i+1}. {final[i]}')







if __name__ == "__main__":
        main()