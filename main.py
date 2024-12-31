import speech_recognition as sr
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = openai.Client()

recognizer = sr.Recognizer()

def record_audio():
    with sr.Microphone() as source:
        print('Listening...')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    return audio

if __name__ == '__main__':
    audio = record_audio()
    with open('test_audio.wav', 'wb') as ad:
        ad.write(audio.get_wav_data())