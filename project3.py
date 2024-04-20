from spotifyGenerator import SpotifyGenerator
from HashMap import HashMap
from HashMap import Song
from HashMap import get_random_songs_from_playlist
from HashMap import getGenre

def Dijkstra():
    # Create a spotify generator object
    sg = SpotifyGenerator("6yPiKpy7evrwvZodByKvM9", 350)

    # Keep getting inputs, until user inputs something other than 'y'
    result = 'y'
    while result.lower() == 'y':
        song_amount = ""

        # Get and validate input for song number from user
        valid_input = False
        while not valid_input:
            song_amount = input("Enter number of songs (Between 1 and 25) ")
            if song_amount.isnumeric():
                if 1 <= int(song_amount) <= 25:
                    valid_input = True

        # Save it as an int
        song_amount = int(song_amount)
        print("Select a genre you would like a playlist for: ")

        # Show user the acceptable genres
        sg.print_acceptable_genres(song_amount)

        # Get the genre they want
        index = int(input("Index: "))
        sg.select_genre(index)

        # Print those songs
        sg.print_tracks(song_amount)

        # Query user for another input
        result = input("Want to make another playlist? (Y/y) type anything for no")

def Hash():
    songs = get_random_songs_from_playlist("6yPiKpy7evrwvZodByKvM9", 350)

    hash_map = HashMap(50)

    for i in range(len(songs)): # insert all songs in our hash map
        song = Song(songs[i]['name'], getGenre(songs[i]))
        hash_map.insert(song)

    song_number = 0
    while True: # get a valid length for the playlist
        try:
            song_number = int(input("Enter number of songs for playlist (between 1 and 25): "))
            if 1 <= song_number <= 25:
                break  # Valid input, exit loop
            else:
                print("Please enter a number between 1 and 25.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    for i in range(len(hash_map.gen_list)): # print all available genres
        print(f'{i}. {hash_map.gen_list[i]}')
    index = 0
    while True: # get first genre index
        try:
            index = int(input("Enter index of desired genre: "))
            if 0 <= index <= (len(hash_map.gen_list) - 1):
                break  # Valid input, exit loop
            else:
                print(f"Invalid index. Please enter a number between 0 and {len(hash_map.gen_list) - 1}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


    final = hash_map.search(hash_map.gen_list[index])
    while len(final) < song_number: # get more genres if first genre doesn't have enough number of songs
        print("Not enough songs in genre")
        ind = 0
        while True:
            try:
                ind = int(input("Enter index of desired genre: "))
                if 0 <= ind <= (len(hash_map.gen_list) - 1):
                    break  # Valid input, exit loop
                else:
                    print(f"Invalid index. Please enter a number between 0 and {len(hash_map.gen_list) - 1}.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        a = hash_map.search(hash_map.gen_list[ind])
        for item in a:
            if item not in final:
                final.append(item)

    for i in range(song_number):
        print(f'{i + 1}. {final[i]}') # print out the playlist


def main():

    option = int(input("Enter the number of the method to find genre\n 1.Dijkstra's algorithm\n 2.HashMap "))
    if option == 1:
        Dijkstra()
    if option == 2:
        Hash()









if __name__ == "__main__":
    main()
