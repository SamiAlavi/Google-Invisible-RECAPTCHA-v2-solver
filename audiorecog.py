from subprocess import call
from os import remove
import speech_recognition as sr

def recog():
    # convert wav to mp3
    call('ffmpeg -i captcha.mp3 -acodec pcm_s16le -ac 1 -ar 16000 captcha.wav')

    r = sr.Recognizer()
    file_audio = sr.AudioFile('captcha.wav')

    with file_audio as source:
       audio_text = r.record(source)

    txt = r.recognize_google(audio_text)
    remove('captcha.wav')
    return txt
