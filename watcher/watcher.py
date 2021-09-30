from .helper import displayFrame, recvFrame
import cv2
from .constants import *
import socket


def connectToServer(ip = SHARER_IP, port = SHARER_PORT):
    """
    Connects to the server
    """

    global SHARER_IP, SHARER_PORT

    SHARER_IP, SHARER_PORT = ip ,port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((SHARER_IP, SHARER_PORT))

    # Starts watching
    watchWebCam(soc)


def watchWebCam(soc):
    """
    Starts watching the camera web
    """

    # Some initial things

    # Recv the len of the web cam resolution string (we receiving the len of the web cam resultion string only as 1 byte
    # because the len will not be bigger than 1 byte presentation ability (0 - 128)
    webCamResolutionLen = int.from_bytes(soc.recv(1), 'big') 

    # Recv the screen size of the sharing
    WEBCAM_SHARING_WIDTH, WEBCAM_SHARING_HEIGHT = soc.recv(webCamResolutionLen).decode().split(' ')

    # Convert the screen size from str to int
    WEBCAM_SHARING_WIDTH = int(WEBCAM_SHARING_WIDTH)
    WEBCAM_SHARING_HEIGHT = int(WEBCAM_SHARING_HEIGHT)

    print(
        f"Start watching on {WEBCAM_SHARING_WIDTH}:{WEBCAM_SHARING_HEIGHT}")

    while True:
        frame = recvFrame(soc)
        displayFrame(frame, "webCamSharing")

        if cv2.getWindowProperty("webCamSharing", cv2.WND_PROP_VISIBLE) <1:
            print("Web camera sharing window has been closed")
            break


def main(ip = SHARER_IP, port = SHARER_PORT):
    global SHARER_IP, SHARER_PORT
    SHARER_IP = ip
    SHARER_PORT = port

    connectToServer()


if __name__ == "__main__":
    main()
