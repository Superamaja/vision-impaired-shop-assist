"""
Optical Character Recognition (OCR) for the Vision-Impaired Shopping Assistant.

This module provides text detection and recognition capabilities using Tesseract OCR.
It includes confidence filtering, text-to-speech integration, and performance monitoring
with decorators for debugging.
"""

import time
from functools import wraps

import pytesseract

from ..config import Config


def timeit(message=None):
    """
    Decorator to measure and print execution time of functions.

    Only prints timing information when DEBUG mode is enabled in Config.
    Useful for performance monitoring during development.

    Args:
        message (str, optional): Custom message to display with timing

    Returns:
        function: Decorated function with timing capability
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not Config.DEBUG:
                return func(*args, **kwargs)

            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            print(
                f"{message}: {duration:.4f}s"
                if message
                else f"{func.__name__} took {duration:.4f}s"
            )
            return result

        return wrapper

    return decorator


class TextDetector:
    """
    Handles text detection and recognition from image frames using OCR.

    This class processes camera frames to detect and extract text, with
    confidence-based filtering and integration with text-to-speech for
    accessibility. It tracks text changes to avoid repetitive announcements.

    Attributes:
        config (dict): Configuration settings for OCR processing
        tts_manager: Text-to-speech manager for audio output
        last_text (str): Last successfully detected text to prevent repetition
    """

    def __init__(self, config=None, tts_manager=None):
        """
        Initialize the text detector with optional configuration and TTS.

        Args:
            config (dict, optional): OCR configuration settings
            tts_manager (TTSManager, optional): TTS manager for speech output
        """
        self.config = config or {}
        self.tts_manager = tts_manager
        self.last_text = ""

    @timeit("OCR Time")
    def get_boxes(self, frame):
        """
        Extract text bounding boxes from an image frame using OCR.

        Performs Tesseract OCR on the input frame and filters results
        by confidence level and removes empty text entries.

        Args:
            frame: Input image frame for text detection

        Returns:
            dict: Filtered OCR data with text boxes and confidence scores
        """
        data = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)
        data = self._filter_confidence(data)
        return self._filter_blank(data)

    def process_frame(self, frame):
        """
        Process a frame for text detection and trigger TTS if text changes.

        Performs OCR on the frame, extracts text, and uses text-to-speech
        to announce new text when it differs from the previously detected text.
        This prevents repetitive announcements of the same content.

        Args:
            frame: Input image frame for processing

        Returns:
            tuple: (boxes, text) where boxes contains OCR data and text is the extracted string
        """
        boxes = self.get_boxes(frame)
        text = " ".join(boxes.get("text", []))

        if text and text != self.last_text and self.tts_manager:
            tts_message = Config.TTS_OCR_TEMPLATE.format(text=text)
            self.tts_manager.say_async(tts_message)
            self.last_text = text
        elif not text:
            self.last_text = ""

        return boxes, text

    def get_average_confidence(self, data):
        """
        Calculate the average confidence score from OCR data.

        Args:
            data (dict): OCR data dictionary containing confidence scores

        Returns:
            float: Average confidence score, or 0 if no confidence data available
        """
        return sum(data["conf"]) / len(data["conf"]) if data["conf"] else 0

    def _filter_confidence(self, data, min_conf=60):
        """
        Filter OCR results by confidence threshold.

        Removes low-confidence text detections to improve accuracy
        and reduce false positives in text recognition.

        Args:
            data (dict): Raw OCR data from Tesseract
            min_conf (int): Minimum confidence threshold (0-100)

        Returns:
            dict: Filtered OCR data containing only high-confidence results
        """
        return {
            k: [v[i] for i, conf in enumerate(data["conf"]) if float(conf) > min_conf]
            for k, v in data.items()
        }

    def _filter_blank(self, data):
        """
        Remove empty or whitespace-only text entries from OCR data.

        Cleans up OCR results by removing entries that contain only
        whitespace or are completely empty.

        Args:
            data (dict): OCR data dictionary

        Returns:
            dict: Cleaned OCR data with empty text entries removed
        """
        return {
            k: [v[i] for i, text in enumerate(data["text"]) if text.strip()]
            for k, v in data.items()
        }
