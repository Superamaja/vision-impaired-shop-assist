import time

import cv2

from src.camera.camera_manager import CameraManager
from src.config import Config
from src.image_processing.image_processor import ImageProcessor
from src.ocr.text_detector import TextDetector
from src.speech.tts_manager import TTSManager
from src.visualization.display import DisplayManager
from src.visualization.text_overlay import TextOverlay
from src.web.api import start_server


def main():
    # Config.enable_debug()
    start_server()

    camera = CameraManager()
    display = DisplayManager()
    text_detector = TextDetector()
    tts = TTSManager()

    fps = 0
    frame_time = time.time()

    try:
        camera.initialize()
        last_text = ""

        while True:
            ret, frame = camera.get_frame()
            if not ret:
                break

            # Calculate FPS
            current_time = time.time()
            fps = 1 / (current_time - frame_time)
            frame_time = current_time

            # Process frame
            processed_frame, normalized = ImageProcessor.preprocess(frame)
            boxes = text_detector.get_boxes(processed_frame)
            text = " ".join(boxes.get("text", []))

            # Only speak if text changed
            if text and text != last_text:
                tts.say_async(text)
                last_text = text

            # Display results
            if Config.DEBUG:
                annotated_frame = TextOverlay.draw_boxes(frame, boxes, draw_text=True)
                annotated_frame = TextOverlay.draw_fps(annotated_frame, fps)
                display.show("Debug", annotated_frame)
                display.show("Normalized", normalized)
                display.show("Processed", processed_frame)

                if text:
                    print(f"Detected text: {text}")
                    print(
                        f"Average confidence: {text_detector.get_average_confidence(boxes):.2f}"
                    )

            else:
                display.cleanup()

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        display.cleanup()


if __name__ == "__main__":
    main()
