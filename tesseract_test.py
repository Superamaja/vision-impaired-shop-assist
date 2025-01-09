import cv2
import numpy as np
import pytesseract
from PIL import Image

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("Original", frame)

    # Make a copy for drawing boxes
    display = frame.copy()

    # Get text and bounding boxes
    d = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)

    # Draw rectangles around text
    n_boxes = len(d["text"])
    for i in range(n_boxes):
        if int(d["conf"][i]) > 0:  # Filter some noise
            (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
            cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                display,
                d["text"][i],
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    # Show frame with boxes
    cv2.imshow("Text Detection", display)

    # Print detected text
    text = pytesseract.image_to_string(frame)
    if text.strip():  # Only print if there's actual text
        print(text)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
