import speech_recognition as sr
import openai
from dotenv import load_dotenv, find_dotenv
from io import BytesIO

_ = load_dotenv(find_dotenv())
client = openai.Client()

recognizer = sr.Recognizer()

def record_audio():
    with sr.Microphone() as source:
        print('Listening...')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    return audio

def audio_to_text(audio):
    wav_data = BytesIO(audio.get_wav_data())
    wav_data.name = 'audio.wav'
    transcription = client.audio.transcriptions.create(
        model='whisper-1',
        file=wav_data,
    )

    return transcription.text


if __name__ == '__main__':
    audio = record_audio()
    transcription = audio_to_text(audio)
    print(transcription)