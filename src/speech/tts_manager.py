"""
Text-to-Speech management for the Vision-Impaired Shopping Assistant.

This module provides thread-safe text-to-speech functionality using pyttsx3,
with configurable speech rate and non-blocking audio output to ensure
the main application remains responsive during speech synthesis.
"""

from threading import Thread

import pyttsx3

from ..config import Config


class TTSManager:
    """
    Manages text-to-speech operations in a thread-safe manner.

    This class provides asynchronous speech synthesis to avoid blocking
    the main application thread. It integrates with the Config system
    for dynamic speech rate adjustments.

    Attributes:
        engine: pyttsx3 TTS engine instance
        _tts_thread: Background thread for speech synthesis
    """

    def __init__(self):
        """
        Initialize the TTS manager with a pyttsx3 engine.

        The engine is configured with settings from the Config class
        and prepared for thread-safe operation.
        """
        self.engine = pyttsx3.init()
        self._tts_thread = None

    def say_async(self, text):
        """
        Speak text asynchronously without blocking the main thread.

        If the TTS engine is already speaking, the new text is ignored
        to prevent overlapping speech.

        Args:
            text (str): The text to speak
        """
        if self._tts_thread and self._tts_thread.is_alive():
            return  # Skip if still speaking

        self._tts_thread = Thread(target=self._speak, args=(text,), daemon=True)
        self._tts_thread.start()

    def _speak(self, text):
        """
        Internal method to handle the actual speech synthesis.

        This method runs in a separate thread and updates engine
        settings before speaking to ensure current configuration is used.

        Args:
            text (str): The text to synthesize
        """
        self._update_configs()
        self.engine.say(text)
        self.engine.runAndWait()

    def _update_configs(self):
        """
        Update TTS engine settings from the current configuration.

        This ensures that any runtime configuration changes are
        applied before speech synthesis begins.
        """
        self.engine.setProperty("rate", Config.TTS_SPEED)
