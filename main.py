"""
Main entry point for the Vision-Impaired Shopping Assistant.

This application provides real-time assistance for vision-impaired users while shopping
by combining OCR text detection and barcode scanning capabilities. It uses computer vision
to read text from product labels and packages, while simultaneously accepting barcode input
through a scanner or manual entry.

Key Features:
- Real-time OCR text detection and text-to-speech output
- Threaded barcode scanning with database lookup
- Web-based configuration and barcode management interface
- Configurable TTS templates and processing parameters
- Debug visualization for development and testing

The application runs multiple components concurrently:
- Camera capture and OCR processing (main thread)
- Barcode input handling (background thread)
- Web API server (background thread)
- Text-to-speech synthesis (background thread)
"""

import time

import cv2

from src.barcode.input_handler import BarcodeInputHandler
from src.camera.camera_manager import CameraManager
from src.config import Config
from src.db.models import DatabaseManager
from src.image_processing.image_processor import ImageProcessor
from src.ocr.text_detector import TextDetector
from src.speech.tts_manager import TTSManager
from src.visualization.display import DisplayManager
from src.visualization.text_overlay import TextOverlay
from src.web.api import start_server


def main():
    """
    Main application entry point and execution loop.

    Initializes all system components, starts the web API server and barcode handler,
    then enters the main processing loop for camera capture and OCR text detection.
    Handles graceful shutdown and resource cleanup.
    """
    # Uncomment to enable debug visualization windows
    # Config.enable_debug()

    # Start the web API server for configuration and barcode management
    start_server()

    # Initialize shared components that will be used across multiple modules
    db_manager = DatabaseManager()
    tts_manager = TTSManager()

    # Initialize barcode input handler with shared dependencies
    # This runs in a background thread to avoid blocking camera operations
    barcode_handler = BarcodeInputHandler(
        db_manager=db_manager, tts_manager=tts_manager
    )
    barcode_handler.start()

    # Initialize camera and display management
    camera = CameraManager()
    display = DisplayManager()
    text_detector = TextDetector(tts_manager=tts_manager)

    # Initialize performance monitoring variables
    fps = 0
    frame_time = time.time()

    try:
        # Initialize camera hardware
        camera.initialize()

        # Main processing loop - continues until 'q' key is pressed
        while True:
            # Capture frame from camera
            ret, frame = camera.get_frame()
            if not ret:
                print("Failed to capture frame, exiting...")
                break

            # Calculate and update FPS for performance monitoring
            current_time = time.time()
            fps = 1 / (current_time - frame_time)
            frame_time = current_time

            # Apply image preprocessing to enhance OCR accuracy
            processed_frame, normalized = ImageProcessor.preprocess(frame)

            # Perform OCR text detection and trigger TTS if new text is found
            boxes, text = text_detector.process_frame(processed_frame)

            # Handle debug visualization if enabled
            if Config.DEBUG:
                # Draw bounding boxes and text on the original frame
                annotated_frame = TextOverlay.draw_boxes(frame, boxes, draw_text=True)
                annotated_frame = TextOverlay.draw_fps(annotated_frame, fps)

                # Show multiple processing stages for debugging
                display.show("Debug", annotated_frame)
                display.show("Normalized", normalized)
                display.show("Processed", processed_frame)

                # Print detected text and confidence metrics to console
                if text:
                    print(f"Detected text: {text}")
                    # Calculate and display confidence only if detection data exists
                    if boxes.get("conf"):
                        avg_conf = text_detector.get_average_confidence(boxes)
                        print(f"Average confidence: {avg_conf:.2f}")
                    else:
                        print(
                            "Average confidence: N/A (no text detected with sufficient confidence)"
                        )
            else:
                # Clean up debug windows if debug mode is disabled
                display.cleanup()

            # Check for 'q' key press to exit application
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Exit key pressed, shutting down...")
                break

    finally:
        # Ensure proper cleanup of all resources
        print("Cleaning up resources...")
        barcode_handler.stop()  # Stop barcode input thread
        camera.release()  # Release camera hardware
        display.cleanup()  # Close debug windows


if __name__ == "__main__":
    main()
