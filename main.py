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
    # Config.enable_debug()
    start_server()

    # Initialize shared components
    db_manager = DatabaseManager()
    tts_manager = TTSManager()

    # Initialize barcode input handler with shared components
    barcode_handler = BarcodeInputHandler(
        db_manager=db_manager, tts_manager=tts_manager
    )
    barcode_handler.start()

    camera = CameraManager()
    display = DisplayManager()
    text_detector = TextDetector(tts_manager=tts_manager)

    fps = 0
    frame_time = time.time()

    try:
        camera.initialize()

        while True:
            ret, frame = camera.get_frame()
            if not ret:
                break

            # Calculate FPS
            current_time = time.time()
            fps = 1 / (current_time - frame_time)
            frame_time = current_time

            # Process frame using ImageProcessor
            processed_frame, normalized = ImageProcessor.preprocess(frame)

            # Use TextDetector to get boxes, text, and handle TTS
            boxes, text = text_detector.process_frame(processed_frame)

            # Display results
            if Config.DEBUG:
                annotated_frame = TextOverlay.draw_boxes(frame, boxes, draw_text=True)
                annotated_frame = TextOverlay.draw_fps(annotated_frame, fps)
                display.show("Debug", annotated_frame)
                display.show("Normalized", normalized)
                display.show("Processed", processed_frame)

                if text:
                    print(f"Detected text: {text}")
                    # Ensure boxes is not empty before calculating confidence
                    if boxes.get("conf"):
                        print(
                            f"Average confidence: {text_detector.get_average_confidence(boxes):.2f}"
                        )
                    else:
                        print(
                            "Average confidence: N/A (no text detected with sufficient confidence)"
                        )

            else:
                display.cleanup()

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        barcode_handler.stop()
        camera.release()
        display.cleanup()


if __name__ == "__main__":
    main()
