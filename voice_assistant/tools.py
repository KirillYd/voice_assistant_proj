import webbrowser

import requests
import speech_recognition
from translate import Translator


def location():
    translator = Translator(to_lang="ru")
    response = requests.get(f"http://ip-api.com/json")
    result = response.json()
    city = translator.translate(result['city'])
    return city


def callback(url):
    webbrowser.open_new(url)


def city_translate(text):
    translator = Translator(to_lang="en", from_lang='ru')
    city = translator.translate(text)
    return city


def record_and_recognize_audio(*args: tuple):
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        return recognized_data
