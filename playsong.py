import os
import random
import pygame
import time

# Set the path to your downloads folder
DOWNLOADS_FOLDER = "downloads/"

def play_random_mp3():
    # Get a list of all files in the downloads folder
    mp3_files = [file for file in os.listdir(DOWNLOADS_FOLDER) if file.endswith(".mp3")]

    # Check if there are any mp3 files in the downloads folder
    if mp3_files:
        # Choose a random mp3 file
        random_mp3 = random.choice(mp3_files)

        # Get the full path to the random mp3 file
        mp3_path = os.path.join(DOWNLOADS_FOLDER, random_mp3)

        # Initialize pygame mixer
        pygame.mixer.init()

        try:
            # Load and play the random mp3 file
            print("Playing Song...")
            pygame.mixer.music.load(mp3_path)
            pygame.mixer.music.play()

            # Wait for 30 seconds
            time.sleep(30)

            # Stop the music playback after 30 seconds
            pygame.mixer.music.stop()
            print("Stopped Song...")

        except pygame.error as e:
            print("Error playing audio:", e)
    else:
        print("No mp3 files found in the downloads folder.")

if __name__ == "__main__":
    play_random_mp3()
