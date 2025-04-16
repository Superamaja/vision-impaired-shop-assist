import time
from functools import wraps

import pytesseract

from ..config import Config

# Add import for TTSManager if type hinting is desired, otherwise optional
# from ..speech.tts_manager import TTSManager


def timeit(message=None):
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
    def __init__(self, config=None, tts_manager=None):
        self.config = config or {}
        self.tts_manager = tts_manager
        self.last_text = ""

    @timeit("OCR Time")
    def get_boxes(self, frame):
        data = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)
        data = self._filter_confidence(data)
        return self._filter_blank(data)

    def process_frame(self, frame):
        """Processes a frame for text, performs OCR, and speaks if text changes."""
        boxes = self.get_boxes(frame)
        text = " ".join(boxes.get("text", []))

        if text and text != self.last_text and self.tts_manager:
            self.tts_manager.say_async(text)
            self.last_text = text
        elif not text:
            self.last_text = ""

        return boxes, text

    def get_average_confidence(self, data):
        return sum(data["conf"]) / len(data["conf"]) if data["conf"] else 0

    def _filter_confidence(self, data, min_conf=60):
        return {
            k: [v[i] for i, conf in enumerate(data["conf"]) if float(conf) > min_conf]
            for k, v in data.items()
        }

    def _filter_blank(self, data):
        return {
            k: [v[i] for i, text in enumerate(data["text"]) if text.strip()]
            for k, v in data.items()
        }
