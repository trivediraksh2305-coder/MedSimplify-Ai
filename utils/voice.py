# utils/voice.py

from gtts import gTTS
import tempfile
import os

def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text[:1000], lang=lang)
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix='.mp3'
        )
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        return None

def speech_to_text():
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=5)
        text = recognizer.recognize_google(audio)
        return text