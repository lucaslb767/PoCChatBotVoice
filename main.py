import speech_recognition as sr
import openai
from dotenv import load_dotenv, find_dotenv
from io import BytesIO
import playsound
from pathlib import Path

_ = load_dotenv(find_dotenv())
client = openai.Client()

recognizer = sr.Recognizer()
AUDIO_FILE = 'Assitant_voice.mp3'
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

def ai_answer_text(messages):
    answer = client.chat.completions.create(
        messages=messages,
        model='gpt-4o-mini',
        max_tokens=1000,
        temperature=0
    )
    return answer

def ai_answer_audio(text):
    if Path(AUDIO_FILE).exists():
        Path(AUDIO_FILE).unlink()
    answer = client.audio.speech.create(
        model='tts-1',
        voice='alloy',
        input=text
    )
    answer.write_to_file(AUDIO_FILE)

def play_audio():
    
    playsound.playsound(AUDIO_FILE)

if __name__ == '__main__':
    messages = []

    while True:
        audio = record_audio()
        transcription = audio_to_text(audio)
        messages.append({'role': 'user', 'content': transcription})
        print(f'User: {messages[-1]['content']}')
        answer = ai_answer_text(messages)
        messages.append({'role': 'assistant', 'content': answer.choices[0].message.content})
        print(f'Bot: {messages[-1]['content']}')
        ai_answer_audio(messages[-1]['content'])
        play_audio()