from spotifyGenerator import SpotifyGenerator


def main():
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


if __name__ == "__main__":
    main()
