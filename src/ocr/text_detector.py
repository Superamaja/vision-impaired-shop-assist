import pytesseract


class TextDetector:
    def __init__(self, config=None):
        self.config = config or {}

    def get_boxes(self, frame):
        data = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)
        data = self._filter_confidence(data)
        return self._filter_blank(data)

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
