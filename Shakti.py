import pyttsx3
import datetime
import os
import webbrowser
import smtplib
import random
import wolframalpha
import wikipedia
import geocoder
import speech_recognition as sr
import sys
import pyautogui
import time 
import json               
engine = pyttsx3.init('sapi5')
client = wolframalpha.Client('6VRXP5-PWVX3THEYP')

voices = engine.getProperty('voices')
# Use print(voices[1].id) to check available voices.
learned_data_file = 'learned_commands.json'


def load_learned_data():
    try:
        with open(learned_data_file, 'r') as file:
            learned_data = json.load(file)
        return learned_data
    except FileNotFoundError:
        return {}

def save_learned_data(data):
    with open(learned_data_file, 'w') as file:
        json.dump(data, file)

def learn_command():
    speak('Sure, please tell me the new command.')
    new_command = myCommand().lower()
    speak('What should be my response to this command?')
    new_response = myCommand()
    
    learned_data = load_learned_data()
    learned_data[new_command] = new_response
    save_learned_data(learned_data)
    speak('I have learned the new command.')

def execute_command(query):
    learned_data = load_learned_data()
    if query in learned_data:
        speak('Executing the learned command.')
        speak(learned_data[query])
    else:
        speak('I do not know how to respond to this command.')

def capture_interactions():
    speak('Capture interactions mode activated. Please speak your command, and I will capture it.')
    new_command = myCommand().lower()
    speak('Please speak your response to this command.')
    new_response = myCommand()
    
    learned_data = load_learned_data()
    learned_data[new_command] = new_response
    save_learned_data(learned_data)
    speak('Interaction captured and learned. You can exit this mode.')

def speak(audio):
    print('SHAKTI: ' + audio)
    engine.say(audio)
    engine.runAndWait()
def load_learned_data():
    try:
        with open(learned_data_file, 'r') as file:
            learned_data = json.load(file)
        return learned_data
    except FileNotFoundError:
        return {}


def greetMe():
    currentH = datetime.datetime.now().hour
    if 0 <= currentH < 12:
        speak('Hello sir, Good Morning!')
    elif 12 <= currentH < 18:
        speak('Hello sir, Good Afternoon!')
    else:
        speak('Hello sir, Good Evening!')

greetMe()
speak('I am SHAKTI, your personal assistant!')
speak('How may I help you?')

def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')
    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query = input('Command: ')
    return query
from geopy.geocoders import GoogleV3

# Set up the Google Maps Geocoding API client with my API key
google_maps_api_key = 'YOUR_GOOGLE_MAPS_API_KEY'
geolocator = GoogleV3(api_key=google_maps_api_key)


if __name__ == '__main__':
    while True:
        query = myCommand().lower()

        if 'learn command' in query:
            learn_command()

        # we can add more conditions for other commands here
        

        elif 'execute command' in query:
            speak('Sure, please specify the command you want me to execute.')
            command_to_execute = myCommand().lower()
            execute_command(command_to_execute)
       

        if 'find my location' in query:
            speak('Sure, let me find your current location.')
            try:
                g = geocoder.ip('me')  # Get the location based on IP address
                location = g.json  # Get location data as JSON
                if location:
                    city = location['city']
                    state = location['state']
                    country = location['country']
                    district = location.get('district', 'N/A') 
                    speak(f'Your current address is in {district}, {city}, {state}, {country}.')
                else:
                    speak("I'm sorry, I couldn't determine your current location.")
            except Exception as e:
                print(e)
                speak("I encountered an error while trying to find your location.")
        
        
        
        elif 'open youtube' in query:
            speak('Okay')
            webbrowser.open('https://www.youtube.com')

        elif 'open google' in query:
            speak('Okay')
            webbrowser.open('https://www.google.co.in')

        elif 'open gmail' in query:
            speak('Okay')
            webbrowser.open('https://www.gmail.com')

        elif "what's up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))

        elif 'email' in query:
            speak('Who is the recipient? ')
            recipient = input('Recipient: ')

            if 'me' in recipient:
                try:
                    speak('What should I say? ')
                    content = input('Content: ')
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login("Your_Username", 'Your_Password')
                    server.sendmail('Your_Username', "Recipient_Username", content)
                    server.close()
                    speak('Email sent!')

                except Exception as e:
                    print(e)
                    speak('Sorry Sir! I am unable to send your message at this moment!')

        elif 'nothing' in query or 'abort' in query or 'stop' in query or 'bye jeevaa'in query or 'No' in query:
            speak('Okay')
            speak('Bye Sir, have a good day, Love you sir.')
            sys.exit()

        elif 'hello' in query:
            speak('Hello Sir')

        elif 'good bye' in query:
            speak('Bye Sir, have a good day, I am always here for you sir!')
            sys.exit()

        elif 'play music' in query:
            speak('Sure! What song would you like to listen to on YouTube?')
            song_name = myCommand()
            webbrowser.open(f'https://www.youtube.com/results?search_query={song_name}+music')
            speak(f'Playing music for "{song_name}" on YouTube. Enjoy!')


        elif 'search' in query:
            search_query = query.replace('search', '')
            webbrowser.open(f'https://www.google.com/search?q={search_query}')

        elif 'tell me about' in query:
            topic = query.replace('tell me about', '')
            try:
                results = wikipedia.summary(topic, sentences=2)
                speak('Got it.')
                speak(f'WIKIPEDIA says - {results}')
            except Exception as e:
                print(e)
                speak('Sorry, I couldn\'t find information about that.')

        elif 'what is' in query:
            question = query.replace('what is', '')
            try:
                res = client.query(question)
                answer = next(res.results).text
                speak('WOLFRAM-ALPHA says - ')
                speak('Got it.')
                speak(answer)
            except Exception as e:
                print(e)
                speak('Sorry, I don\'t have information about that.')

        elif 'open notepad' in query:
            speak('Opening Notepad.')
            os.system('start notepad.exe')

        elif 'open calculator' in query:
            speak('Opening Calculator.')
            os.system('start calc.exe')

        
        elif 'type message' in query:
            speak('Sure, please dictate the message.')
            message = myCommand()
            if message:
                speak('Please specify the application to type the message in, for example, "Notepad" or "Word."')
                app_name = myCommand().lower()
                if app_name == 'notepad':
                    speak('Opening Notepad for typing.')
                    os.system('start notepad.exe')
                    time.sleep(2)  # Wait for Notepad to open
                    pyautogui.typewrite(message)
                elif app_name == 'word':
                    speak('Opening Microsoft Word for typing.')
                    os.system('start winword.exe')
                    time.sleep(2)  # Wait for Word to open
                    pyautogui.typewrite(message)
                else:
                    speak('I am not sure which application you want to use. Please specify "Notepad" or "Word".')
        else:
            speak('Searching...')
            try:
                res = client.query(query)
                answer = next(res.results).text
                speak('WOLFRAM-ALPHA says - ')
                speak('Got it.')
                speak(answer)
            except Exception as e:
                print(e)
                
        speak('Do you have any other command for me, Sir?')

