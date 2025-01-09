import cv2


class CameraManager:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = None

    def initialize(self):
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera {self.camera_id}")
        return self.cap

    def get_frame(self):
        if self.cap is None:
            raise RuntimeError("Camera not initialized")
        return self.cap.read()

    def release(self):
        if self.cap:
            self.cap.release()
            self.cap = None
