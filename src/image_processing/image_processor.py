import cv2

from ..config import Config


class ImageProcessor:
    @staticmethod
    def preprocess(frame):
        """Apply preprocessing steps to the frame."""
        # # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Normalize image to 0-255 range
        normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

        # Apply thresholding
        thresholded = ImageProcessor._threshold(
            normalized, threshold=Config.THRESHOLDING
        )

        return thresholded, normalized

    @staticmethod
    def _threshold(frame, threshold=127):
        """Apply thresholding to the frame. Anything below the threshold will be set to 0 (black)."""
        _, thresholded = cv2.threshold(frame, threshold, 255, cv2.THRESH_BINARY)
        return thresholded
