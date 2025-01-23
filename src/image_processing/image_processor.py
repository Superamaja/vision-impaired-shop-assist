import cv2


class ImageProcessor:
    @staticmethod
    def preprocess(frame):
        """Apply preprocessing steps to the frame."""
        # # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Normalize image to 0-255 range
        normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

        # Apply thresholding
        thresholded = ImageProcessor._threshold(normalized, threshold=70)

        return thresholded, normalized

    @staticmethod
    def _threshold(frame, threshold=127):
        """Apply thresholding to the frame."""
        _, thresholded = cv2.threshold(frame, threshold, 255, cv2.THRESH_BINARY)
        return thresholded
