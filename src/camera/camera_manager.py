"""
Camera management for the Vision-Impaired Shopping Assistant.

This module provides a high-level interface for camera operations,
handling video capture initialization, frame retrieval, and cleanup
with proper error handling.
"""

import cv2


class CameraManager:
    """
    Manages camera operations for video capture and frame processing.

    This class provides a simple interface for camera initialization,
    frame capture, and resource cleanup. It handles common camera
    errors and ensures proper resource management.

    Attributes:
        camera_id (int): Camera device ID (0 for default camera)
        cap (cv2.VideoCapture): OpenCV video capture object
    """

    def __init__(self, camera_id=0):
        """
        Initialize the camera manager with a specific camera device.

        Args:
            camera_id (int): Camera device ID, defaults to 0 (primary camera)
        """
        self.camera_id = camera_id
        self.cap = None

    def initialize(self):
        """
        Initialize the camera capture device.

        Returns:
            cv2.VideoCapture: The initialized video capture object

        Raises:
            RuntimeError: If the camera fails to open
        """
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera {self.camera_id}")
        return self.cap

    def get_frame(self):
        """
        Capture a single frame from the camera.

        Returns:
            tuple: (ret, frame) where ret is success boolean and frame is the image

        Raises:
            RuntimeError: If the camera is not initialized
        """
        if self.cap is None:
            raise RuntimeError("Camera not initialized")
        return self.cap.read()

    def release(self):
        """
        Release the camera resources and cleanup.

        This method should be called when finished using the camera
        to properly release system resources.
        """
        if self.cap:
            self.cap.release()
            self.cap = None
