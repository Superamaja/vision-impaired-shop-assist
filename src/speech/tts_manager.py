import time
from threading import Thread

import pyttsx3


class TTSManager:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._tts_thread = None

    def say_async(self, text):
        if self._tts_thread and self._tts_thread.is_alive():
            return  # Skip if still speaking

        self._tts_thread = Thread(target=self._speak, args=(text,), daemon=True)
        self._tts_thread.start()

    def _speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
