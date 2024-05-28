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

# Initialize the mixer
mixer.init()

# Function to convert text to speech and play it
def talk(audio):
    print(audio)
    # Convert the text to speech
    text_to_speech = gTTS(text=audio, lang='en-uk')
    # Save the speech audio into a file
    text_to_speech.save('audio.mp3')
    # Load the audio file
    mixer.music.load("audio.mp3")
    # Play the audio file
    mixer.music.play()

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
        # Record audio from the microphone
        audio = r.listen(source)
        print("analyzing...")

    try:
        # Recognize speech using Google Speech Recognition
        command = r.recognize_google(audio).lower()
        print("You said: " + command + "\n")
        # Pause before the next command
        time.sleep(2)

    # Exception handling for unrecognized speech
    except sr.UnknownValueError:
        print("Your last command couldn't be heard")
        # If the speech is not recognized, repeat the listening process
        command = myCommand()

    return command

def tars(command):
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

    # If the command is 'open google and search'
    elif 'open google and search' in command:
        # Use regular expression to find the search term in the command
        reg_ex = re.search("open google and search (.*)", command)
        # Split the command to get the search term
        search_for = command.split("search", 1)[1].strip()
        print(search_for)
        # Base URL for Google
        url = "https://www.google.com/search?q=" + search_for
        # Use the talk function to say "Okay!"
        talk("Okay!")
        # Initialize the Firefox webdriver
        driver = webdriver.Firefox()  # Assumes geckodriver is in PATH
        # Open the constructed Google search URL
        driver.get(url)
        # Wait for a few seconds to see the results
        time.sleep(5)
        # Close the browser
        driver.quit()
    # If the command is not recognized
    else:
        # Use the talk function to say a random error message
        talk(random.choice(errors))

talk("TARS activated!")

# loop to continue executing multiple commands
while True:
    time.sleep(4)
    tars(myCommand())
