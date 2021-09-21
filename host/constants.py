import cv2

HOST_IP = "127.0.0.1"
HOST_PORT = 44444

_cam = cv2.VideoCapture(0)

WEBCAM_WIDTH = int(_cam.get(cv2.CAP_PROP_FRAME_WIDTH))
WEBCAM_HEIGHT = int(_cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
