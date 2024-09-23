import speech_recognition as sr  # recognize speech
import playsound  # to play an audio file
from gtts import gTTS  # google text to speech
import random
import webbrowser  # open browser
import os
import time
from datetime import datetime

# Class to store user's information
class person:
    name = ''
    
    def setName(self, name):
        self.name = name

# Function to check if a term exists in voice data
def there_exists(terms, voice_data):
    for term in terms:
        if term in voice_data:
            return True
    return False

r = sr.Recognizer()  # initialize a recognizer

# Listen for audio and convert it to text:
def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError:  # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down')  # error: recognizer is not connected
        print(f">> {voice_data.lower()}")  # print what the user said
        return voice_data.lower()

# Get a string and make an audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')  # text to speech (voice)
    r = random.randint(1, 100)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)  # save as mp3
    playsound.playsound(audio_file)  # play the audio file
    print(f"Assistant: {audio_string}")  # print what the assistant said
    os.remove(audio_file)  # remove audio file

# Respond to voice data
def respond(voice_data):
    # 1: Greeting
    if there_exists(['hey', 'hi', 'hello'], voice_data):
        greetings = [
            f"Hey, how can I help you {person_obj.name}?",
            f"Hey, what's up? {person_obj.name}",
            f"I'm listening {person_obj.name}",
            f"How can I help you? {person_obj.name}"
        ]
        greet = greetings[random.randint(0, len(greetings) - 1)]
        speak(greet)

    # 2: Asking for the assistant's name
    if there_exists(["what is your name", "what's your name", "tell me your name"], voice_data):
        if person_obj.name:
            speak("My name is Alexa.")
        else:
            speak("My name is Alexa. What's your name?")

    # 3: User tells their name
    if there_exists(["my name is"], voice_data):
        person_name = voice_data.split("is")[-1].strip()
        speak(f"Okay, I will remember that {person_name}.")
        person_obj.setName(person_name)  # remember name in person object

    # 4: Search Google
    if there_exists(["search for", "google"], voice_data):
        search_term = voice_data.split("for")[-1].strip()  # Get the search term after 'search for'
        url = f"https://www.google.com/search?q={search_term}"
        speak(f"Here is what I found for {search_term} on Google")
        webbrowser.get().open(url)  # Open the browser to the search results

    # 5: Search YouTube
    if there_exists(["youtube"], voice_data):
        search_term = voice_data.split("for")[-1].strip()  # Get the search term after 'search for'
        url = f"https://www.youtube.com/results?search_query={search_term}"
        speak(f"Here is what I found for {search_term} on YouTube")
        webbrowser.get().open(url)  # Open the browser to the YouTube search results

    # 6: Get current time
    if there_exists(["what time is it", "tell me the time", "current time"], voice_data):
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    # 7: Get today's date
    if there_exists(["what is the date", "today's date", "tell me the date"], voice_data):
        today = datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")

    # 8: Reminder functionality
    if there_exists(["remind me to", "set a reminder to"], voice_data):
        reminder_text = voice_data.split("to")[-1].strip()
        speak(f"Reminder set: {reminder_text}")
        # Here you can add more functionality to store and notify later

# Initialize the person object
person_obj = person()

# Example loop to keep the assistant running
while True:
    voice_data = record_audio()  # get user input
    respond(voice_data)  # respond to user
