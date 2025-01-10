import cv2

from src.camera.camera_manager import CameraManager
from src.ocr.text_detector import TextDetector
from src.speech.tts_manager import TTSManager
from src.visualization.display import DisplayManager
from src.visualization.text_overlay import TextOverlay


def main():
    camera = CameraManager()
    display = DisplayManager()
    text_detector = TextDetector()
    tts = TTSManager()

    try:
        camera.initialize()
        last_text = ""

        while True:
            ret, frame = camera.get_frame()
            if not ret:
                break

            boxes = text_detector.get_boxes(frame)
            text = " ".join(boxes.get("text", []))

            # Only speak if text changed
            if text and text != last_text:
                tts.say_async(text)
                last_text = text

            # Display results
            annotated_frame = TextOverlay.draw_boxes(frame, boxes, draw_text=True)
            display.show("Detected Text", annotated_frame)

            print(f"Detected text: {text}")

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        display.cleanup()


if __name__ == "__main__":
    main()
