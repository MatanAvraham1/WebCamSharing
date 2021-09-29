import pickle
from zlib import decompress
import cv2

def recvall(conn, length):
    """ Retreive all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf

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



def displayFrame(frame, windowName):
    """
    Displays the frame

    param 1: frame from the web camera
    """

    # mat = np.array(frame)  # Not necessary
    cv2.imshow(windowName, frame)
    cv2.waitKey(1)
