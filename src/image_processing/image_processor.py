"""
Image preprocessing for the Vision-Impaired Shopping Assistant.

This module provides image processing utilities to enhance frames for better
OCR accuracy. It includes grayscale conversion, normalization, and thresholding
operations with configurable parameters.
"""

import cv2

from ..config import Config


class ImageProcessor:
    """
    Static utility class for image preprocessing operations.

    This class provides methods to prepare camera frames for optimal
    text recognition by applying various computer vision techniques
    such as grayscale conversion, normalization, and thresholding.
    """

    @staticmethod
    def preprocess(frame):
        """
        Apply comprehensive preprocessing to enhance frame for OCR.

        Performs a series of image processing operations to improve text
        recognition accuracy including grayscale conversion, normalization,
        and adaptive thresholding.

        Args:
            frame (numpy.ndarray): Input BGR color image frame

        Returns:
            tuple: (processed_frame, normalized_frame) where processed_frame
                  is ready for OCR and normalized_frame is for visualization
        """
        # Convert to grayscale
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
        """
        Apply binary thresholding to enhance text contrast.

        Converts grayscale image to binary (black and white) by setting
        pixels below the threshold to black and above to white. This
        enhances text readability for OCR processing.

        Args:
            frame (numpy.ndarray): Grayscale input image
            threshold (int): Threshold value (0-255), defaults to 127

        Returns:
            numpy.ndarray: Binary thresholded image
        """
        _, thresholded = cv2.threshold(frame, threshold, 255, cv2.THRESH_BINARY)
        return thresholded
