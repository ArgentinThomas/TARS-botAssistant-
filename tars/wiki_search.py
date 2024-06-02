import wikipediaapi
from gtts import gTTS
from pygame import mixer
import os
import threading
import time

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

def search_wikipedia(query):
    # Set the user agent
    user_agent = 'TARSBot/1.0 (https://yourdomain.com)'

    # Initialize the Wikipedia API with the user agent
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent=user_agent
    )

    page = wiki_wiki.page(query)

    if not page.exists():
        print(f"No Wikipedia page found for '{query}'")
        return
    
    intro = page.summary.split('\n')[0]  # Take the first paragraph as the intro
    print(intro)
    
    # Generate a unique filename using the current timestamp
    filename = f"speech_{time.strftime('%Y%m%d%H%M%S')}.mp3"
    language = 'en'
    myobj = gTTS(text=intro, lang=language, slow=False)   
    myobj.save(filename)
    
    # Start a new thread to play the audio file
    audio_thread = threading.Thread(target=play_audio, args=(filename,))
    audio_thread.start()
    audio_thread.join()  # Ensure the audio thread completes before proceeding
