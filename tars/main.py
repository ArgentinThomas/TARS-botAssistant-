# main.py

# Importing necessary libraries
import random  # For generating random numbers
import re  # For regular expression operations
import time  # For time-related tasks
from selenium import webdriver  # For web automation tasks
from selenium.webdriver.common.by import By  # For locating elements by their attributes
from selenium.webdriver.common.keys import Keys  # For keyboard key constants
from gtts import gTTS  # Google Text-to-Speech
import speech_recognition as sr  # Speech recognition library
from pygame import mixer  # Pygame mixer for playing audio
import os  # For file operations
from datetime import datetime  # For generating unique filenames
import threading  # For threading operations
import sys  # For system operations
from selenium.common.exceptions import WebDriverException  # For handling WebDriver exceptions

# Importing custom modules
from web_search import open_browser_and_search

# Initialize the mixer
mixer.init()

def play_audio(filename):
    try:
        # Load the audio file
        mixer.music.load(filename)
        # Play the audio file
        mixer.music.play()
        # Wait until the audio finishes playing
        while mixer.music.get_busy():
            time.sleep(1)
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        # Unload the audio file
        mixer.music.unload()
        # Ensure the file is removed
        try:
            os.remove(filename)
        except Exception as e:
            print(f"Error removing audio file: {e}")

# Function to convert text to speech and play it
def talk(audio):
    print(audio)
    # Convert the text to speech
    text_to_speech = gTTS(text=audio, lang='en-uk')
    # Generate a unique filename using the current timestamp
    filename = f"audio_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    # Save the speech audio into a file
    text_to_speech.save(filename)
    # Start a new thread to play the audio file
    audio_thread = threading.Thread(target=play_audio, args=(filename,))
    audio_thread.start()
    audio_thread.join()  # Ensure the audio thread completes before proceeding

# Function to listen for voice commands
def myCommand():
    "listens for commands"
    # Initialize the recognizer
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("TARS is Ready...")
        r.pause_threshold = 1
        # Adjust the recognizer sensitivity to ambient noise and record audio
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        # Record audio from the microphone
        audio = r.listen(source)
        print("Analyzing...")

    try:
        # Recognize speech using Google Speech Recognition
        command = r.recognize_google(audio).lower()
        print("You said: " + command + "\n")
        return command

    except sr.RequestError:
        # API was unreachable or unresponsive
        print("API unavailable")
        return None

    except sr.UnknownValueError:
        # Speech was unintelligible
        print("Your last command couldn't be heard")
        return None

def remove_audio_files():
    # Remove all .mp3 files in the directory
    for filename in os.listdir():
        if filename.endswith(".mp3"):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Error removing file {filename}: {e}")

def tars(command):
    if command is None:
        return

    # List of error messages to use if the command is not recognized
    errors = [
        "I don't know what you mean",
        "Excuse me?",
        "Can you repeat it please?",
    ]

    # if statements for executing commands based on the input 'command'
    if command in ['greet', 'hello', 'hi']:
        talk('Hello! I am TARS. How can I help you?')

    elif command == 'goodbye':
        talk('Goodbye!')
        time.sleep(2)  # Give time to play the goodbye message
        remove_audio_files()  # Remove audio files before exiting
        sys.exit()

    # If the command is 'open google and search'
    elif 'open google and search' in command:
        # Use regular expression to find the search term in the command
        reg_ex = re.search("open google and search (.*)", command)
        # Split the command to get the search term
        search_for = command.split("search", 1)[1].strip()
        print(search_for)
        # Use the talk function to say "Okay!"
        talk("Okay!")
        # Announce what the bot is searching for
        talk(f"I started to search for {search_for}")
        # Start a new thread to open the browser and search
        browser_thread = threading.Thread(target=open_browser_and_search, args=(search_for,))
        browser_thread.start()
        browser_thread.join()  # Wait for the browser thread to finish
    # If the command is not recognized
    else:
        # Use the talk function to say a random error message
        talk(random.choice(errors))

talk("TARS activated!")

# loop to continue executing multiple commands
while True:
    time.sleep(4)
    command = myCommand()
    if command:
        tars(command)
