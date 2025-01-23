import cv2


class TextOverlay:
    @staticmethod
    def draw_boxes(frame, boxes, color=(0, 255, 0), thickness=2, draw_text=False):
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
