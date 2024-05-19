import time
from gtts import gTTS  # Google Text-to-Speech
import speech_recognition as sr  # Speech recognition library
from pygame import mixer  # Pygame mixer for playing audio

# Function to convert text to speech and play it
def talk(audio):
    print(audio)
    # Loop through each line in the input text
    for line in audio.splitlines():
        # Convert the text to speech
        text_to_speech = gTTS(text=audio, lang='en-uk')
        # Save the speech audio into a file
        text_to_speech.save('audio.mp3')
        # Initialize the mixer
        mixer.init()
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
    errors=[
        "I don't know what you mean",
        "Excuse me?",
        "Can you repeat it please?",
    ]
    # TODO: Add if statements here for executing commands based on the input 'command'
    # For example:
    # if command == 'greet':
    #     print('Hello!')
    # elif command == 'goodbye':
    #     print('Goodbye!')
    # else:
    #     print(random.choice(errors))