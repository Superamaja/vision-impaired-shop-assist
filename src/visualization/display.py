import cv2


class DisplayManager:
    def __init__(self):
        self.windows = set()

    def show(self, name, frame):
        self.windows.add(name)
        cv2.imshow(name, frame)

    def cleanup(self):
        cv2.destroyAllWindows()
        self.windows.clear()
