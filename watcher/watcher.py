from watcher.helper import displayFrame, recvFrame
import cv2
from constants import *
import socket


def connectToServer():
    """
    Connects to the server
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((SHARER_IP, SHARER_PORT))

    # Starts watching
    watchWebCam(soc)


def watchWebCam(soc):
    """
    Starts watching the camera web
    """

    # Some initial things
    # Recv the screen size of the sharing
    WEBCAM_SHARING_WIDTH, WEBCAM_SHARING_HEIGHT = soc.recv(
        1024).decode().split(' ')

    # Convert the screen size from str to int
    WEBCAM_SHARING_WIDTH = int(WEBCAM_SHARING_WIDTH)
    WEBCAM_SHARING_HEIGHT = int(WEBCAM_SHARING_HEIGHT)

    print(
        f"Starting watch on {WEBCAM_SHARING_WIDTH}:{WEBCAM_SHARING_HEIGHT}")

    while True:
        frame = recvFrame(soc)
        displayFrame(frame, "webCamSharing")

        if cv2.getWindowProperty("webCamSharing", cv2.WND_PROP_VISIBLE) <1:
            print("Disconnecting...")
            break


def main(ip = SHARER_IP, port = SHARER_PORT):
    global SHARER_IP, SHARER_PORT
    SHARER_IP = ip
    SHARER_PORT = port

    connectToServer()


if __name__ == "__main__":
    main()
