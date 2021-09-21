from zlib import decompress
import cv2
import constants
import socket
import constants
import numpy as np
import pickle


def recvall(conn, length):
    """ Retreive all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def connectToServer():
    """
    Connects to the server
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((constants.HOST_IP, constants.HOST_PORT))

    # Starts watching
    startWatching(soc)


def startWatching(soc):
    """
    Starts watching the camera web
    """

    # Some initial things
    # Recv the screen size of the sharing
    constants.WEBCAM_SHARING_WIDTH, constants.WEBCAM_SHARING_HEIGHT = soc.recv(
        1024).decode().split(' ')

    # Convert the screen size from str to int
    constants.WEBCAM_SHARING_WIDTH = int(constants.WEBCAM_SHARING_WIDTH)
    constants.WEBCAM_SHARING_HEIGHT = int(constants.WEBCAM_SHARING_HEIGHT)

    print(
        f"Starting watch on {constants.WEBCAM_SHARING_WIDTH}:{constants.WEBCAM_SHARING_HEIGHT}")

    while True:
        frame = recvFrame(soc)
        displayFrame(frame)


def recvFrame(soc):
    """
    Receives and returns frame from the socket

    param 1: the socket connection
    param 1 type: socket.socket
    """

    # Retreive the size of the pixels length, the pixels length and pixels
    size_len = int.from_bytes(soc.recv(1), byteorder='big')
    size = int.from_bytes(soc.recv(size_len), byteorder='big')
    frame_pixels_dumped_compressed = recvall(soc, size)

    frame_pixels_dumped = decompress(frame_pixels_dumped_compressed)
    framePixels = pickle.loads(frame_pixels_dumped)

    return framePixels


def displayFrame(frame):
    """
    Displays the frame

    param 1: frame from the web camera
    """

    # mat = np.array(frame)  # Not necessary
    cv2.imshow("webCamSharing", frame)
    cv2.waitKey(1)


def main():
    connectToServer()


if __name__ == "__main__":
    main()
