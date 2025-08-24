"""
Display management for the Vision-Impaired Shopping Assistant.

This module provides window management for debugging and visualization
of the image processing pipeline. It handles OpenCV window creation,
display operations, and cleanup.
"""

import cv2


class DisplayManager:
    """
    Manages OpenCV display windows for debugging and visualization.

    This class provides a centralized way to manage multiple OpenCV windows
    used for displaying processed frames, debug information, and visual feedback
    during development and debugging.

    Attributes:
        windows (set): Set of active window names for tracking
    """

    def __init__(self):
        """
        Initialize the display manager with empty window tracking.
        """
        self.windows = set()

    def show(self, name, frame):
        """
        Display a frame in a named OpenCV window.

        Creates or updates a window with the given name to show the frame.
        Tracks window names for proper cleanup.

        Args:
            name (str): Name of the window
            frame (numpy.ndarray): Image frame to display
        """
        self.windows.add(name)
        cv2.imshow(name, frame)

    def cleanup(self):
        """
        Close all OpenCV windows and clear tracking.

        This method should be called when shutting down the application
        or when switching out of debug mode to properly release resources.
        """
        cv2.destroyAllWindows()
        self.windows.clear()
