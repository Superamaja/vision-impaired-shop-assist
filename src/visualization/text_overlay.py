"""
Text overlay and visual annotation for the Vision-Impaired Shopping Assistant.

This module provides utilities for drawing visual annotations on frames,
including text bounding boxes, OCR results, and performance metrics
for debugging and development purposes.
"""

import cv2


class TextOverlay:
    """
    Static utility class for drawing visual overlays on image frames.

    This class provides methods to annotate frames with bounding boxes,
    text labels, and performance metrics to aid in debugging and
    visualizing the text detection process.
    """

    @staticmethod
    def draw_boxes(frame, boxes, color=(0, 255, 0), thickness=2, draw_text=False):
        """
        Draw bounding boxes around detected text regions.

        Visualizes OCR detection results by drawing rectangles around
        identified text areas, with optional text labels.

        Args:
            frame (numpy.ndarray): Input image frame
            boxes (dict): OCR bounding box data with 'left', 'top', 'width', 'height', 'text'
            color (tuple): BGR color for boxes and text, defaults to green (0, 255, 0)
            thickness (int): Line thickness for rectangles and text, defaults to 2
            draw_text (bool): Whether to draw detected text labels, defaults to False

        Returns:
            numpy.ndarray: Frame with drawn bounding boxes and optional text
        """
        display = frame.copy()
        for i in range(len(boxes.get("text", []))):
            x = boxes["left"][i]
            y = boxes["top"][i]
            w = boxes["width"][i]
            h = boxes["height"][i]
            cv2.rectangle(display, (x, y), (x + w, y + h), color, thickness)
            if draw_text:
                text = boxes["text"][i]
                cv2.putText(
                    display,
                    text,
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    thickness,
                )
        return display

    @staticmethod
    def draw_fps(frame, fps):
        """
        Draw FPS counter on the frame for performance monitoring.

        Adds a frames-per-second indicator to the top-left corner of the frame
        to monitor application performance during debugging.

        Args:
            frame (numpy.ndarray): Input image frame
            fps (float): Current frames per second value

        Returns:
            numpy.ndarray: Frame with FPS counter overlay
        """
        cv2.putText(
            frame,
            f"FPS: {fps:.2f}",
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )
        return frame
