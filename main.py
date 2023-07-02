import struct
import speech_recognition as sr
import openai
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3
import time

apikey = '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'
openai.api_key = apikey
model = 'text-davinci-003'
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set the speaking rate (words per minute)
engine.setProperty('volume', 1)  # Set the volume (float between 0 and 1)
wake_word = "team sigma"
startup_sound = AudioSegment.from_file("startupsound.wav", format="wav")
r = sr.Recognizer()
mic = sr.Microphone()

def wait_for_keyword():
    with mic as source:
        print("Listening for the word...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text_input = r.recognize_google(audio,language="en-IN")
        if wake_word in text_input.lower():
            return True
        else:
            return False
    except sr.UnknownValueError:
        return False
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return False

count=0
while True:
    # wake word
    while not wait_for_keyword():
        play(startup_sound)
        print("Yes Master!")
        break
    while(count!=5):
        # Listen for user input
        print("Ask me anything...")
        count += 1
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=7.0)
        # Recognize user input
        try:
            text_input = r.recognize_google(audio)
            print(f"User said: {text_input}")
            if "finish" in text_input.lower(): # end word
                play(startup_sound)
                print("Stopping the program...")
                exit()
        except sr.UnknownValueError:
            print("Couldn't recognize the audio...")
            continue
        except sr.RequestError as e:
            print("Could not make requests; {0}".format(e))
            continue
        # user input to OpenAI
        prompt = text_input
        response = openai.Completion.create(
            prompt=prompt,
            model=model,
            max_tokens=2000,
            temperature=0.9,
            n=1,
            stop=['---']
        )
        # text into speech
        for result in response.choices:
            print(result.text)
            text = result.text
            engine.say(text)
            engine.runAndWait()
